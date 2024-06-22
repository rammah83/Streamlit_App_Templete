
import streamlit as st


from src.model import load_model
from src.helper import features, DataToPredict, models


with st.sidebar:
    if st.toggle("Choose Different Model"):
        model_name = st.selectbox("Model", options=models.keys(), index=0)
    else:
        model_name = "model01"


# General Layout
left_col, middle_col, right_col = st.columns(
    [1.5, 1, 1], gap="large", vertical_alignment="top"
)

# Disply Inputs
data = dict.fromkeys(DataToPredict.__fields__.keys())


for i, feat in enumerate(features):
    if isinstance(feat[-1], (int, float)):
        data[feat[0]] = left_col.slider(
            *feat,
        )
    else:
        data[feat[0]] = middle_col.selectbox(*feat, help="Feature Discription")


# Display Prediction
with right_col:
    st.markdown(f"## Prediction")
    model = load_model(model_name)
    X = list(DataToPredict(**data).dict().values())

    try:
        # X = data[:model.n_features_in_]
        result = model.predict([X])
        st.metric("# Prediction", value=result.round(2))
    except ValueError as e:
        # st.exception(e)
        st.metric("# Prediction", value="ERROR")

    with st.expander("See explanation"):
        st.write(list(model.coef_), model.intercept_)
        st.write(model.n_features_in_)
