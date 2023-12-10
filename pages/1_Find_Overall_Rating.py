import streamlit as st
import pickle
import pandas as pd
import base64


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
set_bg('backgrounds/bg2n.jpg')

#Loading the saved Ridge regression model
with open("pickles/ridge_model.pkl", "rb") as model_file:
    loaded_ridge_model = pickle.load(model_file)

#Method to produce new predictions i.e. overall ratings
def predict_ova(dataframe):
    # Use your Ridge Regression model to make predictions
    prediction = loaded_ridge_model.predict(dataframe.iloc[:, -10:])
    return prediction

st.write("# Find Overall Ratings🌟")
st.markdown(
    '''
    :white[**This feature lets you generate overall rating from the information you upload.
    The results are being generated from Ridge Regression model trained on FIFA21 dataset.**]

    :white[**Assuming you are not a beginner to FIFA, we have a download option below so that you can download
    a template in which you can directly fill out the information in corresponding columns.**]

    :white[**Once you are done, you can upload the file from the Upload option and check the results.**]
'''
)


#Download option for user to download template file to match input format
with open('csv/OVA_Template.csv', 'rb') as f:
    st.download_button('Download OVA sheet Template', f, file_name='Template.csv')

#User file upload input
#st.subheaderr("Upload")
uploaded_file = st.file_uploader(":red[Choose CSV file]", type="csv")

#checking upload file and predicting new results from it
if uploaded_file is not None:
    df_uploaded = pd.read_csv(uploaded_file)

    st.write("## Uploaded Information")
    st.dataframe(df_uploaded, hide_index=True)

    predicted_ova = predict_ova(df_uploaded)

    predicted_ova_list = predicted_ova.tolist()

    result_df = pd.DataFrame({
        "Player Name": df_uploaded.iloc[:, 0],
        "Predicted Overall Rating": predicted_ova_list
    })

    result_df['Predicted Overall Rating'] = result_df['Predicted Overall Rating'].astype(int)

    st.write("## Predicted Overall Rating")
    st.dataframe(result_df, hide_index=True)
