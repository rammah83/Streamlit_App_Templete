from cgitb import small
import streamlit as st


page_title = ":green[*A*i]*O*S"
page_caption = "**$P_2O_5$ Analytics**"
page_logo = "./res/img/logo.png"

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


st.set_page_config(**main_config)

st.html(
    """
        <style>
            .st-emotion-cache-1wbqy5l{
                visibility: hidden;
            }
        </style>
        """
)

with st.sidebar:
    st.write("Sbakatak")
    # st.image(image=page_logo, width=35, caption="AiOS")

def main_header():
    with st.container():
        col_logo, col_title, _ = st.columns([3, 2, 1], gap="small")
        # col_logo.image(page_logo, width=60, caption="OIS/M")
        col_title.title(page_title)
        col_title.caption(page_caption)

        st.html("""<div class='fixed-header'/><hr/>""")
        
main_header()