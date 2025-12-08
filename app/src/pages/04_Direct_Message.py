import logging
import time
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

# Call the SideBarLinks from the nav module
SideBarLinks()

st.title("System Admin Messages")
st.caption("Private channel for System Administrators.")

# --- INITIALIZE ADMIN HISTORY ---
# We use a unique key 'admin_history' specific to this page
if "admin_history" not in st.session_state:
    st.session_state.admin_history = [
        {"role": "assistant", "content": "Hello Admin. System status is normal."}
    ]

# --- DISPLAY ADMIN HISTORY ---
for msg in st.session_state.admin_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- HANDLE INPUT ---
if prompt := st.chat_input("Type message as Admin..."):
    
    # 1. Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # 2. Add to Admin history
    st.session_state.admin_history.append({"role": "user", "content": prompt})

    # 3. Simulate Response
    response = f"Admin Log: Received '{prompt}'"
    
    # 4. Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            time.sleep(0.5)
            st.write(response)
    
    # 5. Add assistant response to Admin history
    st.session_state.admin_history.append({"role": "assistant", "content": response})