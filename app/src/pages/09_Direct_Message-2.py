import logging
import time
import streamlit as st
import requests
from modules.nav import SideBarLinks
 
logger = logging.getLogger(__name__)
 
# Call the SideBarLinks from the nav module
SideBarLinks()
 
st.title("System Admin Messages")
st.caption("Private channel for Data Analyst.")
 
API_URL = "http://api:4000/admin/messages"
 
with st.sidebar:
    st.header("Chat Settings")
    current_emp_id = st.number_input("Logged in as (My ID)", value=13, step=1)
    
    recipient_id = st.number_input("Send to (Recipient ID)", value=27, step=1)
    
    if st.button("Refresh Messages"):
        st.rerun()
 
messages_data = []
try:
    response = requests.get(API_URL, params={"empID": current_emp_id})
    
    if response.status_code == 200:
        messages_data = response.json()
        messages_data.sort(key=lambda x: x.get('msgID', 0))
    else:
        st.error(f"Error loading messages: {response.status_code}")
except Exception as e:
    st.error(f"Connection Error: {e}")

if messages_data:
    for msg in messages_data:
        msg_id = msg.get('msgID')
        content = msg.get('content')
        sender = msg.get('sender')
        
        if sender == current_emp_id:
            with st.chat_message("user"):
                st.write(content)
                st.caption(f"Sent by Me (ID: {sender})")
        else:
            with st.chat_message("assistant"):
                st.write(content)
                st.caption(f"From Employee {sender}")
else:
    st.info("No messages found. Start a conversation!")
 
if prompt := st.chat_input("Type your message..."):
    
    with st.chat_message("user"):
        st.write(prompt)
    
    payload = {
        "content": prompt,
        "sender": int(current_emp_id),
        "receiver": [int(recipient_id)] # Backend requires a LIST
    }
    
    try:
        res = requests.post(API_URL, json=payload)
        
        if res.status_code == 201:
            st.success("Sent!")
            st.rerun()
        elif res.status_code == 404:
            st.error("Error: The Recipient or Sender ID does not exist.")
        else:
            st.error(f"Failed to send: {res.status_code}")
            st.write(res.text)
            
    except Exception as e:
        st.error(f"Connection failed: {e}")