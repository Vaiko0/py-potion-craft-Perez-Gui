import plotly.express as px
import streamlit as st
from src.profitability_data import (get_anomalies, load_profitability_data, top_10_profitable_potions)


st.title("Rentabillité des potions")

potions, ingredients, diluants = load_profitability_data()
top_potions = top_10_profitable_potions(potions, ingredients, diluants)
anomalies = get_anomalies()

figure = px.bar(
    top_potions,
    x="benefice",
    y="potion",
    orientation="h",
    text="benefice",
    labels={"benefice": "Profit", "potion": "Potion"},
    title="Top 10 des potions les plus rentables",
)
figure.update_traces(texttemplate="%{text:.2f}", textposition="outside")
figure.update_layout(
    yaxis={"categoryorder": "total ascending"},
    xaxis_title="Profit",
    yaxis_title="Potion",
    showlegend=False,
)

st.plotly_chart(figure, use_container_width=True)

if not anomalies.empty:
    st.subheader("Potions non affichées")
    st.dataframe(anomalies[["potion", "type", "valeur", "action"]].drop_duplicates())