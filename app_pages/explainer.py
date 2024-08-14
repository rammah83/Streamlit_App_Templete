import streamlit as st
from src.helper import models, features
from src.model import load_model, model_coefficients
import pandas as pd
import matplotlib.pyplot as plt


st.subheader("Explain Model Predictions")

with st.sidebar:
    if st.toggle("Choose Different Model"):
        model_name = st.selectbox("Model", options=models.keys(), index=0)
    else:
        model_name = "model01"

model = load_model(model_name)
importances = model_coefficients(model).round(2)

left_col, middle_col, right_col = st.columns(
    [1, 1, 2], gap="medium", vertical_alignment="bottom"
)
with left_col:
    st.write(f"Number of Features: {model.n_features_in_}")
    st.dataframe(importances)
    st.bar_chart(
        importances,
        horizontal=True,
    )
st.write("---")
