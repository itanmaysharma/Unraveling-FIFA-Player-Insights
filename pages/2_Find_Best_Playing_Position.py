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


set_bg('backgrounds/bg1.jpg')



with open("pickles/knn_model.pkl", "rb") as model_file:
    loaded_knn_model = pickle.load(model_file)


def scale_pca(inputs):
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(inputs))
    pca = PCA(n_components=10)
    pca.fit(df_scaled)
    df_pca = pca.transform(df_scaled)
    df_pca = pd.DataFrame(df_pca, columns=['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8', 'PC9', 'PC10'])
    return df_pca


def predict_best(dataframe):
    prediction = loaded_knn_model.predict(dataframe)
    return prediction


st.write("# Find Best Positions 📍")
st.markdown(
    '''
    This feature lets you predict best playing position from the information you upload. 
    The results are being generated from K-Nearest Neighbors model trained on FIFA21 dataset
    with an accuracy of 77%. 

    Assuming you are not a beginner to FIFA, we have a download option below so that you can download 
    a template in which you can directly fill out the information in corresponding columns.

    Once you are done, you can upload the file from the Upload option and check the results.
'''
)


#Download option for user to download template file to match input format
with open('csv/Best Position Template.csv', 'rb') as f:
    st.download_button('Download Best Position sheet Template', f, file_name='Template.csv')

# File Upload Section
st.header("Upload CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Prediction Section
if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    df_uploaded = pd.read_csv(uploaded_file)

    # Display the uploaded DataFrame
    st.write("## Uploaded Data:")
    st.dataframe(df_uploaded, hide_index=True)

    # Scale and PCA
    scaleandpca = scale_pca(df_uploaded.iloc[:, -40:])

    # Make Prediction
    predicted_best = predict_best(scaleandpca)

    predicted_best_list = predicted_best.tolist()

    result_df = pd.DataFrame({
        "Player Name": df_uploaded.iloc[:, 0],
        "Predicted Best Position": predicted_best_list
    })

    # Display the prediction
    st.write("## Predicted Best Position:")
    st.dataframe(result_df, hide_index=True)
