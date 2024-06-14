import numpy as np
import streamlit as st


from utils.config import set_shared_config
from src.model import load_model, predict
from src.helper import features, DataToPredict

set_shared_config()

# General Layout
left_col, middle_col, right_col = st.columns([1.5, 1, 1], gap="large")

# Disply Inputs
data = dict.fromkeys(DataToPredict.__fields__.keys())


for i, feat in enumerate(features):
    if isinstance(feat[-1], float):
        data[feat[0]] = left_col.slider(*feat, )
    else:
        data[feat[0]] = middle_col.selectbox(*feat, help="Feature Discription")


# Display Prediction
with right_col:
    st.markdown(f"## Prediction")
    model = load_model()
    X = list(DataToPredict(**data).dict().values())

    try:
        # X = data[:model.n_features_in_]
        result = model.predict([X])
        st.metric("# Prediction", value=result.round(2))
    except ValueError as e:
        # st.exception(e)
        st.metric("# Prediction", value='ERROR')


with st.sidebar:
    if st.toggle("sbac"):
        st.write(list(model.coef_), model.intercept_)