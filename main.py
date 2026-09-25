import streamlit as st

st.set_page_config(
    page_title="Potion Craft — Archives du Ministère",
    page_icon="🧪",
    layout="wide",
)

st.title("🧪 Potion Craft")
st.caption("Département des Archives Magiques — tableau de bord du grimoire numérique")

st.markdown(
    """
    Ce tableau de bord restructure le classeur historique des potions du Ministère.
    Utilise le menu à gauche pour naviguer entre les sections.
    """
)