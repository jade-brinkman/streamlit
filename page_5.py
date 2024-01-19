import streamlit as st
import sqlite3
import bcrypt
import zxcvbn

# Connexion à la base de données SQLite (création ou connexion à une base de données existante)
conn = sqlite3.connect('user_database.db')
cursor = conn.cursor()

# Création de la table des utilisateurs si elle n'existe pas encore
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        hashed_password TEXT
    )
''')
conn.commit()

def main():
    st.title("Application d'Authentification")

    selected_tab = st.sidebar.selectbox("Sélectionnez une option", ["Connexion", "Inscription"])

    if selected_tab == "Connexion":
        show_login()
    elif selected_tab == "Inscription":
        show_signup()

def show_login():
    st.header("Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if authenticate_user(username, password):
            st.success("Connexion réussie!")
            show_user_list(username)  # Affichez la liste pour tous les utilisateurs connectés
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

def show_user_list(current_user):
    st.header("Liste des utilisateurs")

    users = get_all_users()
    for user in users:
        st.write(f"- {user}")

    # Formulaire pour supprimer un utilisateur
    user_to_delete = st.text_input("Nom d'utilisateur à supprimer")
    if st.button("Supprimer"):
        if user_to_delete:
            delete_user(user_to_delete)
            st.success(f"L'utilisateur {user_to_delete} a été supprimé avec succès.")
        else:
            st.error("Veuillez spécifier un nom d'utilisateur à supprimer.")

def get_all_users():
    cursor.execute('SELECT username FROM users')
    result = cursor.fetchall()
    return [user[0] for user in result]

def delete_user(username_to_delete):
    try:
        cursor.execute('DELETE FROM users WHERE username = ?', (username_to_delete,))
        conn.commit()
        print(f"Utilisateur {username_to_delete} supprimé avec succès.")
    except Exception as e:
        print(f"Erreur lors de la suppression de l'utilisateur {username_to_delete}: {e}")

    print("Affichage de la liste des utilisateurs après suppression :")
    users = get_all_users()
    for user in users:
        print(f"- {user}")

def show_signup():
    st.header("Inscription")
    new_username = st.text_input("Nouveau nom d'utilisateur")
    new_password = st.text_input("Nouveau mot de passe", type="password")
    confirm_password = st.text_input("Confirmer le mot de passe", type="password")

    if st.button("S'inscrire"):
        if new_password == confirm_password:
            if not username_exists(new_username):
                # Vérification de la force du mot de passe
                result = zxcvbn.zxcvbn(new_password)

                if result['score'] >= 3:  # Niveau de force minimum (à ajuster selon vos besoins)
                    create_user(new_username, new_password)
                    st.success("Inscription réussie!")
                else:
                    suggestions = result['feedback']['suggestions']
                    restrictions = []

                    # Ajouter des règles personnalisées ici
                    if len(new_password) < 8:
                        restrictions.append("le mot de passe doit contenir au moins 8 caractères")
                    if not any(char.isdigit() for char in new_password):
                        restrictions.append("le mot de passe doit contenir au moins un chiffre")
                    if not any(char.isupper() for char in new_password):
                        restrictions.append("le mot de passe doit contenir au moins une majuscule")
                    if not any(char.islower() for char in new_password):
                        restrictions.append("le mot de passe doit contenir au moins une minuscule")
                    if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/~`" for char in new_password):
                        restrictions.append("le mot de passe doit contenir au moins un caractère spécial")

                    st.error(f"Le mot de passe est trop faible. Respectez les règles suivantes : {', '.join(restrictions)}")
            else:
                st.error("Ce nom d'utilisateur existe déjà. Veuillez choisir un autre.")
        else:
            st.error("Les mots de passe ne correspondent pas.")

def authenticate_user(username, password):
    cursor.execute('SELECT hashed_password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()

    if result:
        stored_password = result[0]
        return bcrypt.checkpw(password.encode('utf-8'), stored_password)

    return False

def create_user(username, password):
    hashed_password = hash_password(password)
    cursor.execute('INSERT INTO users (username, hashed_password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()

def username_exists(username):
    cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()

    return result[0] > 0

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

if __name__ == "__main__":
    main()
