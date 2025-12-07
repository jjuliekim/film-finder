import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.markdown(f" ## <span style='color:blue;'> Film Finder Admin </span>", unsafe_allow_html=True)
st.markdown(" #### App Versions")
# st.subheader('Currently deployed version and past versions')

# You can access the session state to make a more customized/personalized app experience
#st.write(f"### Hi, {st.session_state['first_name']}!")

st.write('Current Active Version: v2.1.1')
st.write('Deployed on Nov 12., 2025 - 3:34 pm')

st.markdown(" #### History")

st.write("v2.1.0:  \nWithdrawn on Nov 12, 2025 - 2:34 pm  \nDeployed on Sept 02, 2024 - 6:04 pm")

st.button("Restore")

st.write ("v2.0.4:  \nWithdrawn on Sept 02, 2024 - 6:04 pm  \nDeployed on Mar 24, 2024 - 2:34 am")
st.button(" Restore")

st.write ("v2.0.3:  \nWithdrawn on Mar 24, 2024 - 2:34 am  \nDeployed on Dec 13, 2023 - 8:45 pm")
st.button("Restore ")

st.write ("v1.5.6:  \nWithdrawn on Dec 13, 2023 - 8:45 pm  \nDeployed on Jan 12, 2023 - 2:48 am")
st.button("Restore  ")

#st.markdown(f"<span style='color:blue;'>Blue Text </span>", unsafe_allow_html=True)

# the currently deployed version 
#st.text_input(r"$\textsf{\small Enter text here}$")

# restore buttons: 
#st.button("Restore")
