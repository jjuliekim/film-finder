import logging
import streamlit as st
import requests
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

SideBarLinks()

st.markdown(
    f" ## <span style='color:blue;'> Film Finder Admin </span>", unsafe_allow_html=True
)
st.markdown(" #### App Versions")

url = "http://api:4000/employee/versions"

try:
    # 1. Fetch all versions to display
    response = requests.get(BASE_URL)
    response.raise_for_status()
    versions_data = response.json()

    if versions_data:
        # The first item is the Current Active Version.
        current_version = versions_data[0]
        
        st.markdown("---")
        st.markdown(" #### History")

        for v in versions_data[0:]:
            col1, col2 = st.columns([3, 1])

            with col1:
                version_info = f"**Version {v.get('versionID')}**:  \nPublished on {v.get('publishedAt')}  \n_{v.get('description', 'No description')}_"
                st.write(version_info)

            with col2:
                version_id = v.get("versionID")
                if st.button("Restore", key=f"restore_{version_id}"):
                    try:
                        restore_url = f"http://api:4000/employee/versions/{version_id}"
                        restore_response = requests.put(restore_url)
                        restore_response.raise_for_status()

                        st.success(f"Successfully restored version {version_id}!")
                        st.rerun()
                    except Exception as restore_error:
                        st.error(f"Error restoring version: {restore_error}")

            st.divider()

    else:
        st.info("No version history found.")

except Exception as e:
    st.error(f"Error connecting to API: {e}")
