import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import certifi
import ssl


st.title('USA Names Data Analysis')
st.write('1) Dataset Name - USA Names')

ssl_context = ssl.create_default_context(cafile=certifi.where())
df_male = pd.read_csv("https://raw.githubusercontent.com/shashank2325/CMPE-255/main/USAMale_names.csv").drop(columns=['Unnamed: 0'])
df_female = pd.read_csv("https://raw.githubusercontent.com/shashank2325/CMPE-255/main/USAFemale_names.csv").drop(columns=['Unnamed: 0'])
df = pd.concat([df_male, df_female], ignore_index=True)

# Filter the data for California and the name "Michael"
df_ca = df[df['state'] == 'CA']
df_michael_ca = df_ca[df_ca['name'] == 'Michael']

# Create a pivot table for the popularity trend
popularity_trend_michael = df_michael_ca.pivot_table(index='year', columns='gender', values='number', aggfunc='sum').fillna(0)

# Plot the trend using Plotly Express
fig1 = px.line(popularity_trend_michael.reset_index(), x='year', y=['F', 'M'], 
               title='Popularity Trend of the Name "Michael" in California',
               labels={'value': 'Number of Babies', 'variable': 'Gender', 'year': 'Year'})
fig1.update_layout(xaxis_title='Year', yaxis_title='Number of Babies Named Michael')

# Display the plot in Streamlit
st.plotly_chart(fig1)

# Group by year and gender to get the gender distribution
gender_distribution_ca = df_ca.groupby(['year', 'gender'])['number'].sum().unstack().fillna(0)
gender_distribution_ca_melted = gender_distribution_ca.reset_index().melt(id_vars='year', value_vars=['F', 'M'], var_name='gender', value_name='count')

# Create a bar plot for gender distribution
fig2 = px.bar(gender_distribution_ca_melted, x='year', y='count', color='gender', barmode='group',
              title='Gender Distribution of Babies Born in California',
              labels={'count': 'Number of Babies', 'year': 'Year', 'gender': 'Gender'})
fig2.update_yaxes(type='linear')

# Display the plot in Streamlit
st.plotly_chart(fig2)

# Aggregate the number of births for each name and gender
top_names_ca = df_ca.groupby(['name', 'gender'])['number'].sum().reset_index()
top_names_ca = top_names_ca.sort_values(by='number', ascending=False).head(10)

# Create a bar plot for the top names
fig3 = px.bar(top_names_ca, x='name', y='number', color='gender', title='Top Baby Names in California', text='number')
fig3.update_layout(xaxis_title='Name', yaxis_title='Total Number of Babies Named')

# Display the plot in Streamlit
st.plotly_chart(fig3)
# Filter for a specific name and gender
specific_name = 'Michael'
specific_gender = 'M'
df_specific = df[(df['name'] == specific_name) & (df['gender'] == specific_gender)]

# Create a line plot for the popularity of a specific name over the years
fig4 = px.line(df_specific, x='year', y='number', color='state',
               title=f'Popularity of the Name "{specific_name}" ({specific_gender}) Over the Years',
               labels={'number': 'Number of Babies Named', 'year': 'Year'})
fig4.update_layout(xaxis_title='Year', yaxis_title=f'Number of Babies Named {specific_name}')

# Display the plot in Streamlit
st.plotly_chart(fig4)



# Generate a word cloud for the most popular names
names = df['name'].value_counts().to_dict()
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(names)

# Display the word cloud using matplotlib
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Baby Names')

# Display the plot in Streamlit
st.pyplot(plt)


# Filter for a specific name and gender again
df_specific_state = df[(df['name'] == specific_name) & (df['gender'] == specific_gender)]

# Create a bar plot for the popularity of a specific name by state
fig5 = px.bar(df_specific_state.groupby('state')['number'].sum().reset_index(), 
              x='state', y='number', 
              title=f'Popularity of the Name "{specific_name}" ({specific_gender}) by State',
              labels={'number': 'Number of Babies Named', 'state': 'State'})
fig5.update_layout(xaxis_title='State', yaxis_title=f'Number of Babies Named {specific_name}')

# Display the plot in Streamlit
st.plotly_chart(fig5)

# Create a heatmap for the popularity of names over the years
heatmap_data = df.pivot_table(index='name', columns='year', values='number', aggfunc='sum').fillna(0)

# Convert the pivot table to a DataFrame for plotting
heatmap_df = heatmap_data.reset_index().melt(id_vars='name', var_name='year', value_name='popularity')

# Create a heatmap using Plotly Express
fig6 = px.density_heatmap(heatmap_df, x='year', y='name', z='popularity', 
                          title='Name Popularity Heatmap Over the Years',
                          labels={'popularity': 'Popularity', 'year': 'Year', 'name': 'Name'})
fig6.update_layout(xaxis_title='Year', yaxis_title='Name')

# Display the plot in Streamlit
st.plotly_chart(fig6)


st.title('Bike Share Data Analysis')
st.write('2)Dataset Name - San Francisco Ford GoBike Share')

ssl_context = ssl.create_default_context(cafile=certifi.where())
dataset_url = 'https://raw.githubusercontent.com/shashank2325/CMPE-255/main/Bike_Share_SFO_2017.csv'
df1 = pd.read_csv(dataset_url).drop(columns=['Unnamed: 0'])


df1['hour'] = pd.to_datetime(df1['start_date']).dt.hour

fig7 = px.histogram(df1, x='hour', title='Bike Usage Throughout the Day',
                    labels={'hour': 'Hour of the Day'}, nbins=24)
fig7.update_xaxes(range=[0, 23], dtick=1)

st.plotly_chart(fig7)

# Plotting bike usage patterns for subscribers vs customers
fig8 = px.histogram(df1, x='duration_sec', color='subscriber_type',
                    title='Trip Duration by Subscriber Type',
                    labels={'duration_sec': 'Trip Duration (seconds)'},
                    marginal='box', nbins=100)
fig8.update_xaxes(range=[0, df1['duration_sec'].quantile(0.95)])  # Exclude outliers

st.plotly_chart(fig8)

# Plotting the most popular start stations
start_station_counts = df1['start_station_name'].value_counts().reset_index()
start_station_counts.columns = ['Station', 'Count']
fig9 = px.bar(start_station_counts.head(10), x='Station', y='Count',
              title='Top 10 Most Popular Start Stations',
              labels={'Count': 'Number of Trips', 'Station': 'Start Station'},
              color='Count', color_continuous_scale='Blues')

st.plotly_chart(fig9)

# Extracting day of the week from the start_date column
df1['weekday'] = pd.to_datetime(df1['start_date']).dt.day_name()

# Plotting bike usage by day of the week for different subscriber types
fig10 = px.histogram(df1, x='weekday', color='subscriber_type',
                    title='Bike Usage by Day of the Week',
                    category_orders={'weekday': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']},
                    labels={'weekday': 'Day of the Week'})

st.plotly_chart(fig10)

# Grouping data by month to get the count of trips for each month
df1['year_month'] = pd.to_datetime(df1['start_date']).dt.to_period('M')
monthly_trends = df1.groupby('year_month').size().reset_index(name='count')
monthly_trends['year_month'] = monthly_trends['year_month'].astype(str)

# Plotting monthly trends in bike usage
fig11 = px.line(monthly_trends, x='year_month', y='count',
               title='Monthly Trends in Bike Usage',
               labels={'count': 'Number of Trips', 'year_month': 'Month'})

st.plotly_chart(fig11)
