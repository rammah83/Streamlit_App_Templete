import streamlit as st
from src.helper import models, features
from src.model import load_model, model_coefficients
import pandas as pd


st.subheader("Explain Model Predictions")

with st.sidebar:
    if st.toggle("Choose Different Model"):
        model_name = st.selectbox("Model", options=models.keys(), index=0)
    else:
        model_name = "model01"
model = load_model(model_name)

left_col, middle_col, right_col = st.columns([1, 1, 1], gap="large")
with left_col:
    st.write(f"Number of Features: {model.n_features_in_}")
    st.dataframe(model_coefficients(model).round(2))
st.write("---")
