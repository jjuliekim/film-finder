import logging
import streamlit as st
import requests
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

SideBarLinks()

st.markdown(f" ## <span style='color:blue;'> Film Finder Admin </span>", unsafe_allow_html=True)
st.markdown(" #### App Versions")

url = 'http://api:4000/employee/versions'

try:
    response = requests.get(url)
    response.raise_for_status()
    versions_data = response.json()

    if versions_data:
        current_version = versions_data[0]
        
        st.write(f"**Current Active Version: {current_version.get('version_num', 'Unknown')}**")
        st.write(f"Deployed on {current_version.get('publishedAt', 'Unknown')}")
        
        st.markdown("---")
        st.markdown(" #### History")

        for v in versions_data[1:]:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                version_info = f"**{v.get('version_num')}**:  \nDeployed on {v.get('publishedAt')}"
                st.write(version_info)
            
            with col2:
                if st.button("Restore", key=f"restore_{v.get('id')}"):
                    st.success(f"Restoring version {v.get('version_num')}...")
            
            st.divider()

    else:
        st.info("No version history found.")

except Exception as e:
    st.error(f"Error connecting to API: {e}")