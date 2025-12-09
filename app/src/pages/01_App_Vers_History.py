import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.markdown("## Film Finder Admin")
st.markdown("#### App Versions")

# Base URL for the versions endpoint
url = 'http://api:4000/employee/versions'

try:
    response = requests.get(url)
    response.raise_for_status()
    versions_data = response.json()

    if versions_data:
        current_version = versions_data[0]
        
        st.write(f"**Current Active Version: {current_version.get('versionID', 'Unknown')}**")
        st.write(f"Deployed on {current_version.get('publishedAt', 'Unknown')}")
        st.write(f"Description: {current_version.get('description', 'No description.')}")
        
        st.markdown("---")
        st.markdown("### History")

        # Loop through the rest of the versions (History)
        for v in versions_data[1:]:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                version_info = f"**Version {v.get('versionID')}**:  \nDeployed on {v.get('publishedAt')}"
                st.write(version_info)
            
            with col2:
              version_id = v.get('versionID')
              # Restore selected version
              if st.button("Restore", key=f"restore_{version_id}"):
                restore_url = f"{url}/{version_id}"
                try:
                  restore_url = f'http://api:4000/employee/versions/{version_id}'
                  restore_response = requests.put(restore_url)
                  restore_response.raise_for_status()
                        
                  st.success(f"Successfully restored version!")
                  st.rerun()
                except Exception as e:
                  st.error(f"Failed to restore: {e}")
            
            st.divider()

    else:
        st.info("No version history found.")

except Exception as e:
    st.error(f"Error connecting to API: {e}")
