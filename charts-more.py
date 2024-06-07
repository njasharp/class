import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load your data
data_url = "chart_games.csv"  # Replace with your data file path
data = pd.read_csv(data_url)

st.title("More charts Games Market Analysis")
st.divider()

# Sidebar filters
st.sidebar.header('Filter Data')
selected_region = st.sidebar.selectbox('Select Region', data['Region'].unique())
selected_platform = st.sidebar.selectbox('Select Platform', data['Platform'].unique())
selected_metric = st.sidebar.selectbox('Select Metric', ['Downloads', 'Revenue', 'Esports Participation', 'Avg. Weekly Hours'])

# Filter data based on selections
filtered_data = data[(data['Region'] == selected_region) & (data['Platform'] == selected_platform)]

# Column Histogram: Single Variable, Few Items
if st.sidebar.checkbox('Show Column Histogram'):
    fig_hist = px.histogram(filtered_data, x=selected_metric, title=f'{selected_platform} Games in {selected_region} - {selected_metric} Histogram')
    st.plotly_chart(fig_hist)

# Line Histogram: Single Variable, Many Items
if st.sidebar.checkbox('Show Line Histogram'):
    fig_line_hist = px.histogram(filtered_data, x=selected_metric, histnorm='percent', title=f'{selected_platform} Games in {selected_region} - {selected_metric} Line Histogram')
    fig_line_hist.update_traces(cumulative_enabled=True)
    st.plotly_chart(fig_line_hist)

# Scatter Chart: Two Variables
if st.sidebar.checkbox('Show Scatter Chart'):
    fig_scatter = px.scatter(filtered_data, x='Game', y=selected_metric, size=selected_metric, color='Game', title=f'{selected_platform} Games in {selected_region} - {selected_metric} Scatter Plot')
    st.plotly_chart(fig_scatter)

# Bubble Chart: Three Variables
if st.sidebar.checkbox('Show Bubble Chart'):
    fig_bubble = px.scatter(filtered_data, x='Game', y=selected_metric, size='Revenue', color='Game', title=f'{selected_platform} Games in {selected_region} - Bubble Chart')
    st.plotly_chart(fig_bubble)

# Stacked 100% Column Chart: Few Periods, Only Relative Differences Matter
if st.sidebar.checkbox('Show Stacked 100% Column Chart'):
    fig_stacked_100_col = px.bar(filtered_data, x='Game', y=selected_metric, color='Region', text_auto='.2s', title=f'{selected_platform} Games in {selected_region} - Stacked 100% Column Chart')
    fig_stacked_100_col.update_layout(barmode='relative')
    st.plotly_chart(fig_stacked_100_col)

# Stacked Column Chart: Few Periods, Relative and Absolute Differences Matter
if st.sidebar.checkbox('Show Stacked Column Chart'):
    fig_stacked_col = px.bar(filtered_data, x='Game', y=selected_metric, color='Region', title=f'{selected_platform} Games in {selected_region} - Stacked Column Chart')
    st.plotly_chart(fig_stacked_col)

# Stacked 100% Area Chart: Many Periods, Only Relative Differences Matter
if st.sidebar.checkbox('Show Stacked 100% Area Chart'):
    fig_stacked_100_area = px.area(filtered_data, x='Game', y=selected_metric, color='Region', title=f'{selected_platform} Games in {selected_region} - Stacked 100% Area Chart')
    st.plotly_chart(fig_stacked_100_area)

# Stacked Area Chart: Many Periods, Relative and Absolute Differences Matter
if st.sidebar.checkbox('Show Stacked Area Chart'):
    fig_stacked_area = px.area(filtered_data, x='Game', y=selected_metric, color='Region', title=f'{selected_platform} Games in {selected_region} - Stacked Area Chart')
    st.plotly_chart(fig_stacked_area)

# Pie Chart: Static, Simple Share of Total
if st.sidebar.checkbox('Show Pie Chart'):
    fig_pie = px.pie(filtered_data, names='Game', values=selected_metric, title=f'{selected_platform} Games in {selected_region} - {selected_metric} Distribution')
    st.plotly_chart(fig_pie)

# Waterfall Chart: Static, Accumulation or Subtraction to Total
if st.sidebar.checkbox('Show Waterfall Chart'):
    fig_waterfall = go.Figure(go.Waterfall(
        name=selected_metric, orientation="v",
        measure=["relative"] * len(filtered_data),
        x=filtered_data['Game'], y=filtered_data[selected_metric],
        textposition="outside",
        text=filtered_data[selected_metric]
    ))
    fig_waterfall.update_layout(title=f'{selected_platform} Games in {selected_region} - Waterfall Chart')
    st.plotly_chart(fig_waterfall)

# Stacked 100% Column Chart with Subcomponents: Static, Components of Components
if st.sidebar.checkbox('Show Stacked 100% Column Chart with Subcomponents'):
    fig_stacked_100_col_sub = px.bar(filtered_data, x='Game', y=selected_metric, color='Region', text_auto='.2s', title=f'{selected_platform} Games in {selected_region} - Stacked 100% Column Chart with Subcomponents')
    fig_stacked_100_col_sub.update_layout(barmode='stack', barnorm='percent')
    st.plotly_chart(fig_stacked_100_col_sub)

st.markdown(' < select data on sidebar menu')
st.info("built by DW 6-8-24 - v1")