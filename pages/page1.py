import streamlit as st


from utils.config import set_shared_config

set_shared_config()

left_col, middle_col, right_col = st.columns([1, 1, 1], gap="large")
with left_col:
    a = st.slider("Feature A", 0, 100, 10)
    Z = st.slider("Feature B", 0.0, 100.0, (25.0, 75.0))

with middle_col:
    c = st.selectbox(
        "Feature C", ["Triangle", "Cercle", "Squarre"], help="Feature Discription"
    )
    d = st.selectbox(
        "Feature C", ["Apple", "Orange", "Bannane"], help="Feature Discription"
    )

with right_col:
    st.markdown(f"# {a * 2}")
    st.markdown(f"# {(sum(b)/2):.2f}")