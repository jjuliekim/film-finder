import logging
import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

SideBarLinks()

st.markdown(f" ## <span style='color:blue;'> Film Finder Admin </span>", unsafe_allow_html=True)

BASE_URL = "http://api:4000/admin/requests"

current_emp_id = st.session_state.get('empID', 16)
first_name = st.session_state.get('first_name', 'Employee')

st.markdown(f"### {first_name}'s Requests")

try:
    get_url = f"{BASE_URL}/{current_emp_id}"
    response = requests.get(get_url)
    
    if response.status_code == 200:
        requests_data = response.json()
    else:
        requests_data = []

    if requests_data:
        df = pd.DataFrame(requests_data)
        
        st.subheader("Summary")
        if 'status' in df.columns:
            st.table(df['status'].value_counts())
        
        st.markdown("### Request List")

        for req in requests_data:
            r_id = req.get('requestID')
            msg = req.get('message')
            status = req.get('status')
            timestamp = req.get('timestamp')
            user_id = req.get('userID')
            
            col1, col2, col3 = st.columns([3, 1, 1.5])
            
            with col1:
                st.write(f"**From User ID: {user_id}**")
                st.write(f"\"{msg}\"")
                st.caption(f"Time: {timestamp}")
            
            with col2:
                if status == 'resolved':
                    st.success("Resolved")
                else:
                    st.warning(f"Status: {status}")
            
            with col3:
                if status != 'resolved':
                    if st.button("Mark Resolved", key=f"resolve_{r_id}"):
                        update_url = f"{BASE_URL}/{r_id}"
                        update_payload = {"status": "resolved"}
                        
                        try:
                            r = requests.put(update_url, json=update_payload)
                            r.raise_for_status()
                            st.success("Request resolved!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Could not update: {e}")
                else:
                    st.write("No actions available")

            st.divider()
            
    else:
        st.info("No requests found for this employee.")

except Exception as e:
    st.error(f"Connection Error: {e}")