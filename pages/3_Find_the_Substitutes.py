import streamlit as st
import pandas as pd
import base64
import pickle
import unidecode


# Reference: https://discuss.streamlit.io/t/how-do-i-use-a-background-image-on-streamlit/5067?page=2
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


set_bg('backgrounds/fifabg.jpg')

# loading Kmeans model file
with open("pickles/kmeans_model.pkl", "rb") as model_file:
    loaded_kmeans_model = pickle.load(model_file)

# Loading the cluster labels and preprocessed dataset
cluster_labels = loaded_kmeans_model.labels_

df = pd.read_csv('csv/fifa_processed_dataset.csv')

GK = "GK"
DEF = df['Best Position'][df['Best Position'].str.contains(r'B$')].unique()
MID = df['Best Position'][df['Best Position'].str.contains(r'M$')].unique()
FWD = df['Best Position'][df['Best Position'].str.contains(r'F$|S$|T$|W$')].unique()


# categorizing each player into 5 categories
def categorize_positions(positions):
    if positions in GK:
        return "Goalkeeper"
    elif positions in DEF:
        return "Defender"
    elif positions in MID:
        return "Midfielder"
    elif positions in FWD:
        return "Forward"
    else:
        return "Not known"


df['Position Category'] = df['Best Position'].apply(categorize_positions)
df['Name'] = df['Name'].apply(unidecode.unidecode)

# Adding cluster labels to the original DataFrame for all players except Goalkeepers and Not knowns
df = df[df['Position Category'] != "Not known"].copy()
df = df[df['Position Category'] != "Goalkeeper"].copy()
df['Cluster'] = cluster_labels

# New DataFrame with selective relevant features and their cluster value
clusterinfo = df[['ID', 'Name', 'Club', 'Age', 'Position Category', 'OVA', 'Cluster', 'Value', 'Wage']]

st.write("# Find the best alternatives!😉")
st.markdown(
    '''
    **This feature lets you get a list of players which are similar in skills with the name
    you give from player list.**


    :white[**The list in dropdown contain player names and you can type in your favourite and select matching from the list.
    If the name doesn't appear, then apparently he is not in the FIFA database yet.**]

    :white[**The results are being generated from K-Means clustering model trained on FIFA21 dataset.**]

    :white[**Even if you are a beginner to FIFA, this option can help you in selecting a solid set of players.**]

    :white[**Once you have selected the name, just select the number of similar players you want.**]
'''
    , unsafe_allow_html=True)


def return_similar_players(dataf, player, num_results):
    # if the player exists in the DataFrame
    if player not in dataf['Name'].values:
        return "Player not found in the DataFrame"

    # fetching the cluster and value of the target player
    cluster_filter = dataf.loc[df['Name'] == player, 'Cluster'].values[0]

    # Check if there are players in the same cluster
    if cluster_filter not in dataf['Cluster'].values:
        return "No players in the same cluster"

    similar_players = dataf[(dataf['Cluster'] == cluster_filter)]
    similar_players = similar_players.drop('Cluster', axis=1)

    # 'num_results' similar players
    similar_players = similar_players.head(num_results)

    return similar_players.iloc[:, 1:]


my_data = clusterinfo

# Reading a players name from text file and showing it in list options
with open("players.txt", "r") as file:
    players = file.read().splitlines()

player_name = st.selectbox(
    ":white[**Please select your favourite player to find his matches**]",
    players
)

st.divider()

st.write("Showing results for:", player_name)

st.divider()

number = st.number_input(":white[**Enter the count of players you want like the one chosen above**]", value=11)

st.write(":white[**Here are your match results found**]")
st.dataframe(return_similar_players(my_data, player_name, number), hide_index=True)
st.warning(' If the list is short than selected count, that means players are limited for above selections.', icon="❗")
