import streamlit as st
import pandas as pd
import numpy as np

# Titre de la page
st.title("Ma page de données")

# Génération de données factices (remplacez cela par vos propres données)
data = {
    'Nom': ['John', 'Jane', 'Doe', 'Alice', 'Bob'],
    'Âge': [25, 30, 22, 28, 35],
    'Score': [85, 92, 78, 88, 95]
}

df = pd.DataFrame(data)

# Affichage des données dans un tableau
st.write("Voici quelques données :")
st.dataframe(df)

# Affichage d'une carte avec des marqueurs (exemple avec des coordonnées aléatoires)
map_data = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [37.77, -122.4],
    columns=['latitude', 'longitude']
)

st.map(map_data)

# Ajout d'une section avec des graphiques
st.write("Graphiques :")

# Histogramme d'âges
st.bar_chart(df['Âge'])

# Nuage de points entre l'âge et le score
st.scatter_chart(df[['Âge', 'Score']])

# Ajout de widgets interactifs
st.sidebar.header("Filtres")

# Slider pour filtrer les personnes en fonction de l'âge
age_range = st.sidebar.slider("Filtrer par âge", min_value=20, max_value=40, value=(20, 40))
filtered_data = df[(df['Âge'] >= age_range[0]) & (df['Âge'] <= age_range[1])]

# Affichage des données filtrées
st.write(f"Données filtrées pour les personnes âgées entre {age_range[0]} et {age_range[1]} :")
st.dataframe(filtered_data)



