import streamlit as st  # type: ignore

from utils.config import set_shared_config

set_shared_config()


pages = {
    "HOME": [st.Page("./app_pages/home.py", title="Home", icon="🏠")],
    "MODELING": [
        st.Page("./app_pages/predictor.py", title="Predictor", icon="🤖"),
        st.Page("./app_pages/explainer.py", title="Model Explainer", icon="🧮"),
    ],
}

pg = st.navigation(pages, position="sidebar")
pg.run()
