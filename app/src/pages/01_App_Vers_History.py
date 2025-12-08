import logging
import streamlit as st
import requests
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

SideBarLinks()

st.markdown(f" ## <span style='color:blue;'> Film Finder Admin </span>", unsafe_allow_html=True)
st.markdown(" #### App Versions")

# Base URL for the versions endpoint
BASE_URL = 'http://api:4000/employee/versions'

try:
    # 1. Fetch all versions to display
    response = requests.get(BASE_URL)
    response.raise_for_status()
    versions_data = response.json()

    if versions_data:
        # Assume the list is sorted by date (newest first). 
        # The first item is the Current Active Version.
        current_version = versions_data[0]
        
        # Use .get('versionID') based on your SQL schema
        st.write(f"**Current Active Version: {current_version.get('version_num', 'Unknown')}**")
        st.write(f"Deployed on {current_version.get('publishedAt', 'Unknown')}")
        
        st.markdown("---")
        st.markdown(" #### History")

        # Loop through the rest of the versions (History)
        for v in versions_data[1:]:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                version_info = f"**{v.get('version_num')}**:  \nDeployed on {v.get('publishedAt')}"
                st.write(version_info)
            
            with col2:
                # Button unique key using versionID
                if st.button("Restore", key=f"restore_{v.get('versionID')}"):
                    # 2. Logic to restore specific version
                    restore_url = f"{BASE_URL}/{v.get('versionID')}"
                    
                    try:
                        restore_response = requests.put(restore_url)
                        restore_response.raise_for_status()
                        
                        st.success(f"Successfully restored version {v.get('version_num')}!")
                        
                        # Rerun the app to refresh the list and show the new 'Current' version
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Failed to restore: {e}")
            
            st.divider()

    else:
        st.info("No version history found.")

except Exception as e:
    st.error(f"Error connecting to API: {e}")