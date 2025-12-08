import streamlit as st
import pandas as pd
import plotly.express as px
from modules.nav import SideBarLinks

# 1. Navigation
SideBarLinks()

# 2. Page Header
st.markdown("## <span style='color:blue;'> Film Finder User Analytics </span>", unsafe_allow_html=True)

# 3. KPI Section (Hardcoded Numbers)
st.subheader("Key Performance Indicators (for this week)")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Registered Users", value="12,450", delta="15")

with col2:
    st.metric(label="Average Rating", value="4.15", delta="0.5")

with col3:
    st.metric(label="Average Session Time", value="85:03 mins", delta="-23:00")

st.markdown("---")

# 4. Profile Types Chart (Mock Data)
st.subheader("Profile Distribution (Kids vs. Teens vs. Adults)")

# Create simple mock data for the 3 categories
data = {
    'Category': ['For Kids', 'For Teens', 'For Adults'],
    'Count': [4500, 3200, 15300]  # Mock counts
}
df_profiles = pd.DataFrame(data)

# Create a simple Bar Chart
fig = px.bar(
    df_profiles, 
    x='Category', 
    y='Count', 
    title='Number of Profiles by Age Group',
    color='Category',  # This gives each bar a distinct color
    text='Count'       # This puts the number on top of the bar
)

# Clean up the chart look
fig.update_layout(xaxis_title="Profile Type", yaxis_title="Number of Profiles")

# Display the chart
st.plotly_chart(fig, use_container_width=True)