import streamlit as st
import pandas as pd
import plotly.express as px
from modules.nav import SideBarLinks

# 1. Navigation
SideBarLinks()

# 2. Page Header
st.markdown("## <span style='color:blue;'> Film Finder Movie Analytics </span>", unsafe_allow_html=True)

# 3. KPI Section (Hardcoded)
st.subheader("Content Performance")

# Create 4 columns for the requested KPIs
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Top Genre", value="Action")

with col2:
    st.metric(label="Avg. Movie Length", value="1h 54m")

col3, col4 = st.columns(2)

with col3:
    st.metric(label="Most Watched Actor", value="Tom Cruise")

with col4:
    st.metric(label="Top Director", value="Christopher Nolan")

st.markdown("---")

# 4. Chart Section (Mock Data)
# Since you mentioned movies have genres, let's visualize the "Inventory by Genre"
st.subheader("Movie Catalog Distribution by Genre")

# Mock Data
data = {
    'Genre': ['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Horror', 'Animation', 'Thriller'],
    'Count': [320, 210, 245, 180, 95, 150, 110]
}
df_movies = pd.DataFrame(data)

# Create a Bar Chart
fig = px.bar(
    df_movies, 
    x='Genre', 
    y='Count', 
    title='Total Movies Available by Genre',
    color='Count',                 # Color the bars based on the count magnitude
    color_continuous_scale='Blues', # Use a blue color scale to match your theme
    text='Count'                   # Show the number on the bar
)

# Customize layout
fig.update_layout(xaxis_title="Genre", yaxis_title="Number of Movies")

# Display the chart
st.plotly_chart(fig, use_container_width=True)
