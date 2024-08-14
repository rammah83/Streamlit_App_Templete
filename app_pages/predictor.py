import streamlit as st


from src.model import load_model
from src.helper import features, DataToPredict, models


st.title("Make Prediction")

with st.sidebar:
    if st.toggle("Choose Different Model"):
        model_name = st.selectbox("Model", options=models.keys(), index=0)
    else:
        model_name = "model01"

# set general Layout
left_col, middle_col, right_col = st.columns(
    [1.5, 1, 1], gap="large", vertical_alignment="top"
)

# Disply Inputs
left_col.subheader("INPUTS")
inputs = dict.fromkeys(DataToPredict.__fields__.keys())
for key, params in features.items():
    if isinstance(params[0], (int, float)):
        inputs[key] = left_col.slider(
            label=key,
            min_value=params[0],
            max_value=params[1],
            value=params[2],
            help="Feature Discription",
        )
    else:
        inputs[key] = middle_col.selectbox(
            label=key,
            options=params,
            help="Feature Discription",
        )


# Display Prediction
with right_col:
    st.subheader(f"PREDICTION")
    model = load_model(model_name)
    X = list(DataToPredict(**inputs).dict().values())

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
