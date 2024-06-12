import streamlit as st


from utils.config import set_shared_config
from src.model import load_model, predict
from src.helper import features

set_shared_config()

data = [None] * len(features)
left_col, middle_col, right_col = st.columns([1.5, 1, 1], gap="large")

# Inputs
for i, feat in enumerate(features):
    if isinstance(feat[-1], float):
        data[i] = left_col.slider(*feat, )
    else:
        middle_col.selectbox(*feat, help="Feature Discription")

# Prediction
with right_col:
    st.markdown(f"## Prediction")
    model = load_model()
    try:
        X = data[:model.n_features_in_]
        result = model.predict([X])
        st.metric("# Prediction", value=result.round(2))
    except ValueError as e:
        # st.exception(e)
        st.metric("# Prediction", value=-999.99)


with st.sidebar:
    if st.toggle("sbac"):
        st.write(list(model.coef_), model.intercept_)