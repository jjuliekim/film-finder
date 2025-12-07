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

import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks

# set the header of the page
st.markdown(' ### User Requests Data')

#mock data 
data = {
    'Request ID': [101, 102, 103, 104],
    'User': ['dhruvi@gmail.com', 'yasmin@icloud.com', 'emma@hotmail.com', 'julie@gmail.com'],
    'Feature Requested': ['Request Database', 'Export to PDF', 'More Movie Genres', 'Fix Login Bug'],
    'Status': ['Pending', 'In Progress', 'Pending', 'Completed'],
    'Date Submitted': ['2025-11-01', '2025-11-02', '2025-11-03', '2025-11-05']
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
