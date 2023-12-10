import streamlit as st
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
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


set_bg('backgrounds/bg1n.jpg')

#loading saved KNN model from Phase 2
with open("pickles/knn_model.pkl", "rb") as model_file:
    loaded_knn_model = pickle.load(model_file)

#scaling and applying PCA for inputs to match trained model's format expectation
def scale_pca(inputs):
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(inputs))
    pca = PCA(n_components=10)
    pca.fit(df_scaled)
    df_pca = pca.transform(df_scaled)
    df_pca = pd.DataFrame(df_pca, columns=['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8', 'PC9', 'PC10'])
    return df_pca

#Prediction function
def predict_best(dataframe):
    prediction = loaded_knn_model.predict(dataframe)
    return prediction


st.write("# Find Best Position📍")
st.markdown(
    '''
    :white[**This feature lets you predict best playing position from the information you upload.
    The results are being generated from K-Nearest Neighbors model trained on FIFA21 dataset.**]

    :white[**Assuming you are not a beginner to FIFA, we have a download option below so that you can download
    a template in which you can directly fill out the information in corresponding columns.**]

    :white[**Once you are done, you can upload the file from the Upload option and check the results.**]
'''
)

st.warning('Please upload data for atleast 10 players', icon="❗")


#Download option for user to download template file to match input format
with open('csv/Best Position Template.csv', 'rb') as f:
    st.download_button('Download Best Position Input Template', f, file_name='Template.csv')

#user input upload and validation for minimum required input data
#st.header(":red[Upload CSV File]")
uploaded_file = st.file_uploader(":red[**Choose a CSV file**]", type="csv")


if uploaded_file is not None:

    df_uploaded = pd.read_csv(uploaded_file)

    if len(df_uploaded) < 10:
        st.warning("The uploaded file does not have at least 10 samples.")
    else:
        st.success("File successfully uploaded. Check results now.")

        st.write("## Uploaded Data:")
        st.dataframe(df_uploaded, hide_index=True)

        scaleandpca = scale_pca(df_uploaded.iloc[:, -40:])

        predicted_best = predict_best(scaleandpca)

        predicted_best_list = predicted_best.tolist()

        result_df = pd.DataFrame({
            "Player Name": df_uploaded.iloc[:, 0],
            "Predicted Best Position": predicted_best_list
        })


        st.write("## Predicted Best Positions:")
        st.dataframe(result_df, hide_index=True)
