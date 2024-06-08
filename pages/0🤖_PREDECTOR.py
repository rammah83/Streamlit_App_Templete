from json import load
import streamlit as st


from utils.config import set_shared_config
from utils.model import load_model

set_shared_config()

left_col, middle_col, right_col = st.columns([1, 1, 1], gap="large")
with left_col:
    feat_1 = st.slider("Feature A", 0.0, 1.0, 0.1)
    feat_2 = st.slider("Feature B", 0.0, 1.0, 0.1)
    feat_3 = st.slider("Feature C", 0.0, 1.0, 0.1)
    feat_4 = st.slider("Feature D", 0.0, 1.0, 0.1)
    feat_5 = st.slider("Feature E", 0.0, 1.0, 0.1)

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
    result = model.predict([[feat_1, feat_2, feat_3, feat_4, feat_5]])
    st.metric("# Prediction", value=result.round(2))

with st.sidebar:
    if st.toggle("sbac"):
        st.write(list(model.coef_), model.intercept_)
