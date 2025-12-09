import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()
 
st.title("Film Finder Tasks")
BASE_URL = "http://api:4000/admin/tasks"
 
st.markdown("### 1. Add Task")
with st.form("add_task"):
    desc = st.text_input("Description")
    emp_id_add = st.number_input("Assign to Employee ID", value=13, step=1)
    if st.form_submit_button("Create Task"):
        payload = {"empID": int(emp_id_add), "description": desc}
        try:
            res = requests.post(BASE_URL, json=payload)
            if res.status_code in [200, 201]:
                st.success("Task Created!")
            else:
                st.error(f"Error: {res.status_code}")
                st.write(res.text)
        except Exception as e:
            st.error(f"Connection Error: {e}")
 
st.divider()
 
st.markdown("### 2. View Tasks")
 
view_emp_id = st.number_input("View Tasks for Employee ID:", value=13, step=1)
 
if st.button("Load Tasks"):
    try:
        get_url = f"{BASE_URL}/{view_emp_id}"
        response = requests.get(get_url)
        if response.status_code == 200:
            tasks = response.json()
            if tasks:
                for task in tasks:
                    t_id = task.get('taskID')
                    desc = task.get('description')
                    # Display simple list
                    st.info(f"**Task {t_id}:** {desc}")
            else:
                st.warning(f"No tasks found for Employee {view_emp_id}")
        else:
            st.error(f"Could not load tasks. Status: {response.status_code}")
            st.write(response.text)
    except Exception as e:
        st.error(f"System Error: {e}")