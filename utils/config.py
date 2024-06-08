import os
import streamlit as st


page_title = ":green[*A*i]*O*S"
page_caption = "**$P_2O_5$ Analytics**"
page_logo = "./res/img/logo.png"

# check if file exist
if not os.path.exists(page_logo):
    ...


main_config = dict(
    page_title="ANAPHOS",
    page_icon=":shark:",
    layout="wide",  # ["centered", "wide"]
    initial_sidebar_state="auto",
    menu_items={
        "Get Help": "https://www.cyberwolf.net/help",
        "Report a bug": None,  # "https://anaphos.ocpgroup.ma/",
        "About": """#### This is app used to deploy machine learning models for OCP Group.
                    ### 😎 cool app designed and deployeed by OIS/M Team!""",
    },
)


def set_shared_config():
    st.set_page_config(**main_config)
    st.logo(image=page_logo, link=r"http://localhost:8501/")
    st.html(
        """
            <style>
                .st-emotion-cache-1wbqy5l{
                    visibility: hidden;
                }
                .st-emotion-cache-ch5dnh ef3psqc5{
                    visibility: hidden;
                }
            </style>
            """
    )
    with st.sidebar:
        if st.toggle("Activate feature"):
            st.write("Feature activated!")
        else:
            st.write("some thing")

    with st.container():
        col_logo, col_title, _ = st.columns([3, 2, 1], gap="small")
        col_logo.image(page_logo, width=60, caption="OIS/M")
        col_title.title(page_title)
        col_title.caption(page_caption)
        st.html("""<div class='fixed-header'/>""")
        ### Custom CSS for the sticky header
        st.html(
            """
            <style>
            div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
                position: sticky;
                background:green;
                top: 2.875rem;
                background-color: white;
                z-index: 999;
            }
            .fixed-header {
                border-bottom: 1px solid black;
            }
            </style>
            """
        )
