import plotly.express as px
import streamlit as st

from profitability_data import (
    load_profitability_data,
    top_10_profitable_potions,
)


st.title("Potions Profitability")

potions, ingredients, diluants = load_profitability_data()
top_potions = top_10_profitable_potions(potions, ingredients, diluants)

figure = px.bar(
    top_potions,
    x="benefice",
    y="potion",
    orientation="h",
    text="benefice",
    labels={"benefice": "Profit", "potion": "Potion"},
    title="Top 10 Most Profitable Potions",
)
figure.update_traces(texttemplate="%{text:.2f}", textposition="outside")
figure.update_layout(
    yaxis={"categoryorder": "total ascending"},
    xaxis_title="Profit",
    yaxis_title="Potion",
    showlegend=False,
)

st.plotly_chart(figure, use_container_width=True)