import logging
import time
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

# Call the SideBarLinks from the nav module
SideBarLinks()

st.title("Data Analyst Messages")
st.caption("Private channel for Data Analysts.")

# --- INITIALIZE ANALYST HISTORY ---
# We use a DIFFERENT unique key 'analyst_history'
if "analyst_history" not in st.session_state:
    st.session_state.analyst_history = [
        {"role": "assistant", "content": "Hello Analyst. Ready for queries."}
    ]

# --- DISPLAY ANALYST HISTORY ---
for msg in st.session_state.analyst_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- HANDLE INPUT ---
if prompt := st.chat_input("Type message as Analyst..."):
    
    # 1. Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # 2. Add to Analyst history
    st.session_state.analyst_history.append({"role": "user", "content": prompt})

    # 3. Simulate Response
    response = f"Analyst Log: Received '{prompt}'"
    
    # 4. Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Calculating..."):
            time.sleep(0.5) 
            st.write(response)
    
    # 5. Add assistant response to Analyst history
    st.session_state.analyst_history.append({"role": "assistant", "content": response})