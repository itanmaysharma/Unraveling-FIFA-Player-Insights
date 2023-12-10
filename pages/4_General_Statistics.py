import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import base64
import plotly.express as px
import seaborn as sns

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
set_bg('backgrounds/fifa.jpg')

df = pd.read_csv("csv/fifa_processed_dataset.csv")

st.write("# FIFA Player Statistics🌟")

top_play=df[['Name','OVA',"Age",'Club','Best Position']]
top_play.sort_values(by='OVA',ascending=False,inplace=True)
top_30_play=top_play[:100]
fig=px.scatter(top_30_play,x='Age',y='OVA',color='Age',size='OVA',hover_data=['Name','Club','Best Position'],title='Top Football Players in the FIFA 21 game')
st.plotly_chart(fig)

#Plot of Overall ratings
plt.hist(df["OVA"], edgecolor='k')
plt.ylabel("Counts")
plt.xlabel("Overall")
plt.title("Distribution of overall ratings")

st.pyplot(plt.gcf())
plt.clf()

#Displaying top 10 nationalities by player count
s=df.groupby("Nationality").size().reset_index(name="Count").sort_values(by="Count", ascending=False)
s=s[0:10]
plt.bar(s["Nationality"], s["Count"])
plt.xticks(rotation=45)
plt.title("Top ten nationalities by player count")

st.pyplot(plt.gcf())
plt.clf()

#Value versus wage scatter plot
sns.scatterplot(data=df, y="Wage", x="Value", hue="Best Position", size="OVA", sizes=(25, 200), alpha=0.5,legend=False)

plt.title("Value of players by wages paid")
st.pyplot(plt.gcf())
plt.clf()

st.write("# :white[**Best Overall Teams FIFA 21**]")

#Best overall team in FIFA21
final_team=df[['Name','Age','OVA','Best Position','Club']]
final_team.sort_values(by='Age',inplace=True)
pos_play=final_team.groupby('Best Position').apply(lambda x:np.max(x['OVA'])).reset_index(name='Overall Score')
player_pos=pd.merge(final_team,pos_play,how='inner',left_on=['Best Position','OVA'],right_on=['Best Position','Overall Score'])
pos_best=player_pos[['Name','Club','Age','Best Position','Overall Score']]
cm = sns.light_palette("yellow", as_cmap=True)
pos_best.style.background_gradient(cmap=cm)
st.dataframe(pos_best, use_container_width=True)
