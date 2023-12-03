import streamlit as st
import pandas as pd
import base64


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


set_bg_hack('fifabg.jpg')


# st.set_page_config(
#     page_title="Substitutes",
#     page_icon="👋",
# )

st.write("# Find the best alternatives! 👋")


def return_similar_players(df, player, num_results, return_within_fraction):
    # Check if the player exists in the DataFrame
    if player not in df['Name'].values:
        return "Player not found in the DataFrame"

    # Get the cluster and value of the target player
    cluster_filter = df.loc[df['Name'] == player, 'Cluster'].values[0]
    player_value = df.loc[df['Name'] == player, 'Value'].values[0]

    # Check if there are players in the same cluster
    if cluster_filter not in df['Cluster'].values:
        return "No players in the same cluster"

    # Filter for similar players based on cluster and value range
    similar_players = df[(df['Cluster'] == cluster_filter) &
                          (df['Value'] >= player_value * (1 - return_within_fraction)) &
                          (df['Value'] <= player_value * (1 + return_within_fraction))]

    # Get the top 'num_results' similar players
    similar_players = similar_players.head(num_results)

    return similar_players


my_data = pd.read_csv('Cluster_Fifa_New.csv')

with open("players.txt", "r") as file:
    options = file.read().splitlines()

player_name = st.sidebar.selectbox(
    "Please select the preferred player for whom you want likewise list",
    options
)

st.write("Results")
st.table(return_similar_players(my_data, player_name, 100, 0.05))

