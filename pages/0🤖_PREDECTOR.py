from json import load
import streamlit as st


from utils.config import set_shared_config
from src.model import load_model
from src.helper import features

set_shared_config()

X = [None] * len(features)
left_col, middle_col, right_col = st.columns([1, 1, 1], gap="large")
with left_col:
    for i, feat in enumerate(features):
        X[i] = st.slider(*feat)

with middle_col:
    c = st.selectbox(
        "Feature C", ["Triangle", "Cercle", "Squarre"], help="Feature Discription"
    )
    d = st.selectbox(
        "Feature C", ["Apple", "Orange", "Bannane"], help="Feature Discription"
    )

with right_col:
    st.markdown(f"## Prediction")
    model = load_model()
    result = model.predict([X])
    st.metric("# Prediction", value=result.round(2))

with st.sidebar:
    if st.toggle("sbac"):
        st.write(list(model.coef_), model.intercept_)

