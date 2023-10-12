import streamlit as st
import pandas as pd
import plotly.express as px


dataset_url = 'https://raw.githubusercontent.com/shashank2325/CMPE-255/main/Bike_Share_SFO_2017.csv'
df = pd.read_csv(dataset_url).drop(columns=['Unnamed: 0'])


df['hour'] = pd.to_datetime(df['start_date']).dt.hour

fig1 = px.histogram(df, x='hour', title='Bike Usage Throughout the Day',
                    labels={'hour': 'Hour of the Day'}, nbins=24)
fig1.update_xaxes(range=[0, 23], dtick=1)

st.plotly_chart(fig1)

