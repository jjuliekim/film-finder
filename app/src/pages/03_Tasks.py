import streamlit as st
import requests
 
st.title("Film Finder Tasks")
BASE_URL = "http://api:4000/admin/tasks"
 
# --- 1. ADD TASK (POST) ---
# This likely uses the generic URL if your POST route doesn't require an ID in the URL
st.markdown("### 1. Add Task")
with st.form("add_task"):
    desc = st.text_input("Description")
    emp_id_add = st.number_input("Assign to Employee ID", value=13, step=1)
    if st.form_submit_button("Create Task"):
        # Payload usually needs empID inside JSON for POST
        payload = {"empID": int(emp_id_add), "description": desc}
        try:
            # Note: Verify if your POST route is /tasks or /tasks/<id>
            # Assuming POST is to the base /tasks endpoint:
            res = requests.post(BASE_URL, json=payload)
            if res.status_code in [200, 201]:
                st.success("Task Created!")
            else:
                st.error(f"Error: {res.status_code}")
                st.write(res.text)
        except Exception as e:
            st.error(f"Connection Error: {e}")
 
st.divider()
 
# --- 2. VIEW TASKS (GET) ---
st.markdown("### 2. View Tasks")
 
# We need an input here because your Backend REQUIREs an ID to view tasks
view_emp_id = st.number_input("View Tasks for Employee ID:", value=13, step=1)
 
if st.button("Load Tasks"):
    try:
        # CRITICAL FIX: Append the ID to the URL
        # URL becomes: http://api:4000/movie/admin/tasks/13
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