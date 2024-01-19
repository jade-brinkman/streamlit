import streamlit as st
import streamlit.components.v1 as components

# bootstrap 4 collapse example
components.html(
    """
<iframe src="https://snake.googlemaps.com/" width="700" height="700" frameborder="0" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
    """,
    height=718,
    width=718,
)

