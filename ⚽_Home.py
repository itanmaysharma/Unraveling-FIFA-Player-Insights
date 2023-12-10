import streamlit as st
import base64

st.set_page_config(
    page_title="FootForesight Homepage",
    page_icon="👋",
)


st.write("# Welcome to FootForesight👋")

st.markdown(
    '''
    :white[FootForesight is a Web Application which leverages the results
    from the project " From Virtual Pitch to Data: Unraveling FIFA Player Insights".]

    :white[The main objective for the project mentioned was to extract valuable insights from FIFA21 dataset
    by taking advantage of ML models and answers below questions -]

    :white[1. What are the most significant attributes associated with a player and how their overall
       rating is impacted based on these attributes, and can we build a predictive model for
       this?]

    :white[2. What are the attributes affecting a player’s market value and what are the trends in it?]

    :white[3. What are other possible hidden trends in the dataset that can help in improving
       gameplay balance leading to enhanced playing experience?]

    :white[FootForesight is a user-friendly interface which lets you give new data and generate desirable outcomes.]

    :white[There are currently three main features which can be accessed from sidebar.]

    :white[Relevant instructions are mentioned on each page.]
'''
)


#Reference: https://discuss.streamlit.io/t/how-do-i-use-a-background-image-on-streamlit/5067?page=2
def set_bg(main_bg):
    '''
    adding background image
    '''
    # set bg name
    main_bg_ext = "jpg"

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


set_bg('backgrounds/bg4.jpg')

