import pandas as pd
import plotly.express as px
import streamlit as st
from potions_magic_type import load_magic_type_data
from skills import load_skills

df_magic_types, df_potions_inventeurs = load_magic_type_data()
df_skills = load_skills()

competences_par_type = df_magic_types[["type_de_magie", "competences"]].copy()
competences_par_type["competence"] = competences_par_type["competences"].str.split(";")
competences_par_type = competences_par_type.explode("competence")
competences_par_type["competence"] = competences_par_type["competence"].str.strip()

potions_competences = df_potions_inventeurs.merge(
	competences_par_type,
	left_on="type-magie-potion",
	right_on="type_de_magie",
	how="inner",
)
nombre_potions_par_competence = (
	potions_competences.groupby("competence", as_index=False)
	.agg(nombre_potions=("potion", "nunique"))
	.sort_values("competence")
)

figure = px.line_polar(
	nombre_potions_par_competence,
	r="nombre_potions",
	theta="competence",
	line_close=True,
	markers=True,
	title="Nombre de potions par compétence",
	labels={
		"nombre_potions": "Nombre de potions",
		"competence": "Compétence",
	},
)
figure.update_traces(fill="toself")
figure.update_layout(showlegend=False)

st.title("Compétences des potions")
st.plotly_chart(figure, use_container_width=True)

