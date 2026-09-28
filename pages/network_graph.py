import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from network_data import load_data, clean_data, build_graph

st.set_page_config(page_title="Inventors and Potions Graph", layout="wide")
st.title("Graphe de reseau des inventeurs et de leurs potions")

potions, inventors = load_data("data/potions-craft.xlsx")
potions, inventors = clean_data(potions, inventors)

graph = build_graph(potions, inventors)

positions = nx.spring_layout(graph, seed=42)
colors = [attributs["color"] for _, attributs in graph.nodes(data=True)]
sizes = [attributs["size"] * 10 for _, attributs in graph.nodes(data=True)]
labels = {noeud: attributs["label"] for noeud, attributs in graph.nodes(data=True)}

fig, ax = plt.subplots(figsize=(12, 8))
nx.draw(graph, pos=positions, node_color=colors, node_size=sizes, labels=labels, font_size=7, ax=ax)

st.pyplot(fig)

st.markdown("### Lignées")
for nom_lignee, couleur in graph.graph["lineage_colors"].items():
    st.markdown(
        f"<span style='display:inline-block;width:12px;height:12px;"
        f"background-color:{couleur};border-radius:50%;margin-right:8px;'></span>"
        f"{nom_lignee.title()}",
        unsafe_allow_html=True,
    )