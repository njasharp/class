import streamlit as st
import pandas as pd
import plotly.express as px

# Load your data
data_url = "chart_games.csv"
data = pd.read_csv(data_url)

# Streamlit app title
st.title("Charts Games Market Analysis")
st.divider()
# Sidebar filters
st.sidebar.header('Select Chart Filter Data')
selected_region = st.sidebar.selectbox('Select Region', data['Region'].unique())
selected_platform = st.sidebar.selectbox('Select Platform', data['Platform'].unique())
selected_metric = st.sidebar.selectbox('Select Metric', ['Downloads', 'Revenue', 'Esports Participation', 'Avg. Weekly Hours'])

# Filter data based on selections
filtered_data = data[(data['Region'] == selected_region) & (data['Platform'] == selected_platform)]

# Line Chart
if st.sidebar.checkbox('Show Line Chart'):
    fig_line = px.line(filtered_data, x='Game', y=selected_metric, title=f'{selected_platform} Games in {selected_region} - {selected_metric} Line Chart')
    st.plotly_chart(fig_line)

# Column Histogram
if st.sidebar.checkbox('Show Column Histogram'):
    fig_hist = px.histogram(filtered_data, x=selected_metric, title=f'{selected_platform} Games in {selected_region} - {selected_metric} Histogram')
    st.plotly_chart(fig_hist)

# Scatter Chart
if st.sidebar.checkbox('Show Scatter Chart'):
    fig_scatter = px.scatter(filtered_data, x='Game', y=selected_metric, size=selected_metric, color='Game', title=f'{selected_platform} Games in {selected_region} - {selected_metric} Scatter Plot')
    st.plotly_chart(fig_scatter)

# Pie Chart
if st.sidebar.checkbox('Show Pie Chart'):
    fig_pie = px.pie(filtered_data, names='Game', values=selected_metric, title=f'{selected_platform} Games in {selected_region} - {selected_metric} Distribution')
    st.plotly_chart(fig_pie)

# Multiple Bar Charts
if st.sidebar.checkbox('Show Multiple Bar Charts'):
    fig_bar = px.bar(filtered_data, x='Game', y=selected_metric, color='Game', title=f'{selected_platform} Games in {selected_region} - {selected_metric} Bar Chart')
    st.plotly_chart(fig_bar)

# Circular Area Chart
if st.sidebar.checkbox('Show Circular Area Chart'):
    fig_area = px.area(filtered_data, x='Game', y=selected_metric, title=f'{selected_platform} Games in {selected_region} - {selected_metric} Area Chart')
    st.plotly_chart(fig_area)

# Stacked Column Chart
if st.sidebar.checkbox('Show Stacked Column Chart'):
    fig_stacked = px.bar(filtered_data, x='Game', y=selected_metric, color='Region', title=f'{selected_platform} Games in {selected_region} - {selected_metric} Stacked Column Chart')
    st.plotly_chart(fig_stacked)

st.markdown(' < select data on sidebar menu')
st.info("built by DW 6-8-24 - v1")