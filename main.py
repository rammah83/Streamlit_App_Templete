import streamlit as st # type: ignore

from utils.config import set_shared_config

set_shared_config()

# st.logo(page_logo)
# st.title('_Streamlit_ is :blue[cool] :sunglasses:')
# st.subheader("This is our first app with Streamlit!")

pages = {
    "HOME" : [
        st.Page("home.py", title="Home", icon="🏠")
    ],
    "Resources" : [
        st.Page("./pages/predictor.py", title="PREDICTOR", icon="🤖"),
        st.Page("./pages/explainer.py", title="MODEL EXPLAINER", icon="🧮"),
    ]
}

pg = st.navigation(pages, position="sidebar")
pg.run()