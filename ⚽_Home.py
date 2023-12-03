import streamlit as st
import base64

st.set_page_config(
    page_title="FootForesight Homepage",
    page_icon="👋",
)

st.write("# Welcome to FootForesight! 👋")

# st.sidebar.success("Select a demo above.")

st.markdown(
    """
"""
)


def set_bg_hack(main_bg):
    '''
    adding background image
    '''
    # set bg name
    main_bg_ext = "png"

    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


set_bg_hack('bg.png')
