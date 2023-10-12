import streamlit as st
import pandas as pd
import plotly.express as px
import certifi
import ssl

ssl_context = ssl.create_default_context(cafile=certifi.where())
dataset_url = 'https://raw.githubusercontent.com/shashank2325/CMPE-255/main/Bike_Share_SFO_2017.csv'
df = pd.read_csv(dataset_url).drop(columns=['Unnamed: 0'])


df['hour'] = pd.to_datetime(df['start_date']).dt.hour

fig1 = px.histogram(df, x='hour', title='Bike Usage Throughout the Day',
                    labels={'hour': 'Hour of the Day'}, nbins=24)
fig1.update_xaxes(range=[0, 23], dtick=1)

st.plotly_chart(fig1)

# Plotting bike usage patterns for subscribers vs customers
fig2 = px.histogram(df, x='duration_sec', color='subscriber_type',
                    title='Trip Duration by Subscriber Type',
                    labels={'duration_sec': 'Trip Duration (seconds)'},
                    marginal='box', nbins=100)
fig2.update_xaxes(range=[0, df['duration_sec'].quantile(0.95)])  # Exclude outliers

st.plotly_chart(fig2)

# Plotting the most popular start stations
start_station_counts = df['start_station_name'].value_counts().reset_index()
start_station_counts.columns = ['Station', 'Count']
fig3 = px.bar(start_station_counts.head(10), x='Station', y='Count',
              title='Top 10 Most Popular Start Stations',
              labels={'Count': 'Number of Trips', 'Station': 'Start Station'},
              color='Count', color_continuous_scale='Blues')

st.plotly_chart(fig3)

# Extracting day of the week from the start_date column
df['weekday'] = pd.to_datetime(df['start_date']).dt.day_name()

# Plotting bike usage by day of the week for different subscriber types
fig4 = px.histogram(df, x='weekday', color='subscriber_type',
                    title='Bike Usage by Day of the Week',
                    category_orders={'weekday': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']},
                    labels={'weekday': 'Day of the Week'})

st.plotly_chart(fig4)

# Grouping data by month to get the count of trips for each month
df['year_month'] = pd.to_datetime(df['start_date']).dt.to_period('M')
monthly_trends = df.groupby('year_month').size().reset_index(name='count')
monthly_trends['year_month'] = monthly_trends['year_month'].astype(str)

# Plotting monthly trends in bike usage
fig5 = px.line(monthly_trends, x='year_month', y='count',
               title='Monthly Trends in Bike Usage',
               labels={'count': 'Number of Trips', 'year_month': 'Month'})

st.plotly_chart(fig5)



