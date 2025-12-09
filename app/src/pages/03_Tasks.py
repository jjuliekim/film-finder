import logging
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

SideBarLinks()

st.markdown(f" ## <span style='color:blue;'> Film Finder Admin </span>", unsafe_allow_html=True)

st.title("Film Finder Tasks")
API_URL = "http://api:4000/movie/admin/tasks"

with st.form("new_task"):
    desc = st.text_input("New Task Description")
    if st.form_submit_button("Add Task"):
        if desc:
            # We send empID: 1 just to make the database happy
            requests.post(API_URL, json={"empID": 1, "description": desc})
            st.success("Task Added!")
            st.rerun()

st.divider()

# 3. Get All Tasks
try:
    # Fetch data from API
    response = requests.get(API_URL)
    tasks = response.json()

    for task in tasks:
        t_id = task['taskID']
        description = task['description']
        completed_date = task['completedAt']

        col_left, col_right = st.columns([3, 1])

        with col_left:
            st.subheader(description)
            if completed_date:
                st.success(f"Completed on: {completed_date}")
            else:
                st.warning("Pending")

        with col_right:
            if not completed_date:
                if st.button("Mark Done", key=f"btn_done_{t_id}"):
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    requests.put(f"{API_URL}/{t_id}", json={"completedAt": current_time})
                    st.rerun()
            
            # Always show 'Delete' button
            if st.button("Delete", key=f"btn_del_{t_id}"):
                requests.delete(f"{API_URL}/{t_id}")
                st.rerun()

        st.divider()

except Exception as e:
    st.error(f"Could not load tasks: {e}")