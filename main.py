import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Potion Crafting App")

potions_data = pd.read_excel("./data/potions-craft.xlsx", sheet_name="potions")

st.dataframe(potions_data)