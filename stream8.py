import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
data = pd.read_csv('mena_games.csv')

# Streamlit app title
st.title("MENA Games Market Analysis")

# Filter options
platforms = data['Platform'].unique()
regions = data['Region'].unique()
metrics = ['Downloads', 'Revenue', 'Avg. Weekly Hours','Esports Participation']

selected_platform = st.selectbox('Select Platform', platforms)
selected_region = st.selectbox('Select Region', regions)
selected_metric = st.selectbox('Select Metric', metrics)

# Filter data based on selections
filtered_data = data[(data['Platform'] == selected_platform) & (data['Region'] == selected_region)]

# Create charts
st.subheader(f"{selected_platform} Games in {selected_region} - {selected_metric}")

# Bar Chart
fig_bar = px.bar(filtered_data, x='Game', y=selected_metric, color='Game',
                 title=f"{selected_platform} Games in {selected_region} - {selected_metric} Bar Chart")
st.plotly_chart(fig_bar)

# Pie Chart
fig_pie = px.pie(filtered_data, names='Game', values=selected_metric, 
                 title=f"{selected_platform} Games in {selected_region} - {selected_metric} Distribution")
st.plotly_chart(fig_pie)

# Scatter Plot
fig_scatter = px.scatter(filtered_data, x='Game', y=selected_metric, size=selected_metric, color='Game',
                         title=f"{selected_platform} Games in {selected_region} - {selected_metric} Scatter Plot")
st.plotly_chart(fig_scatter)

# Line Chart (if data over time is available)
if 'Date' in filtered_data.columns:
    fig_line = px.line(filtered_data, x='Date', y=selected_metric, color='Game',
                       title=f"{selected_platform} Games in {selected_region} - {selected_metric} Over Time")
    st.plotly_chart(fig_line)
    
st.subheader('Asia & MENA Gaming Markets ')
image_path = "d-market.png"
st.image(image_path, caption='Data 2024 -https://venturebeat.com/games/niko-partners-mena-asia-market-report-2024/', use_column_width=True)

st.title('Niko Partners Report on Asia & MENA Gaming Markets')

# Display the report text
report_text = """
## Key Updates:

- The combined revenue for Asia & MENA gaming markets was $85.5 billion in 2023, marking a 4.6% increase from the previous year.
- For 2024, the forecasted growth rate is 2.5%, with expected revenue reaching $87.6 billion.
- By 2028, the market is projected to approach nearly $100 billion ($97.1 billion) with a CAGR of 2.5%.

## Top Items:

- The number of gamers in Asia & MENA was 1.61 billion in 2023, over half of the world’s total gamers.
- India is projected to contribute 72% of the growth in gamers, adding 277 million new gamers by 2028.
- The MENA region is expected to be the second fastest growing market.
- Mobile gaming dominates with 93.7% of gamers playing on mobile devices.
- By 2028, there will be an estimated 1.87 billion mobile gamers, 606 million PC gamers, and 100 million console gamers.
"""

st.markdown(report_text)