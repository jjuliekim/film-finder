import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.markdown(f" ## <span style='color:blue;'> Film Finder Admin </span>", unsafe_allow_html=True)
# st.subheader('Currently deployed version and past versions')

# You can access the session state to make a more customized/personalized app experience
#st.write(f"### Hi, {st.session_state['first_name']}!")

import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks

# set the header of the page
st.markdown(f"### {st.session_state['first_name']}'s Tasks")
#st.write(f"### Hi, {st.session_state['first_name']}!")

# mock data 
# tasks sql 

#match to er diagram
data = {
    'Taasks ID': [101, 102, 103],
    'Task': ['Database Migration Failure', 'Slow Search complains', 'Profile Merging'],
    'Status': ['Pending', 'In Progress', 'Completed'],
    'Date Submitted': ['2025-11-01', '2025-11-02', '2025-11-05']
}

# dictionary to DataFrame
df = pd.DataFrame(data)
with st.echo(code_location='above'):
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=False,
    )

# Summary
st.subheader("Summary")
with st.echo(code_location='above'):
    # breakdown of requests by status
    df1 = df['Status'].value_counts()
    st.table(df1)
