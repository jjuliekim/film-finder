import logging
import time
import streamlit as st
import requests
from modules.nav import SideBarLinks
 
logger = logging.getLogger(__name__)
 
# Call the SideBarLinks from the nav module
SideBarLinks()
 
st.title("System Admin Messages")
st.caption("Private channel for System Administrators.")
 
# --- CONFIGURATION ---
# Based on your previous turns, the prefix is likely /movie/admin
API_URL = "http://api:4000/admin/messages"
 
# --- SIDEBAR SETTINGS ---
# We need to know who "You" are and who you want to "Talk to"
with st.sidebar:
    st.header("Chat Settings")
    # Default to 27 based on your mock data
    current_emp_id = st.number_input("Logged in as (My ID)", value=27, step=1)
    
    # Default to 17 (another user in your mock data)
    recipient_id = st.number_input("Send to (Recipient ID)", value=17, step=1)
    
    if st.button("Refresh Messages"):
        st.rerun()
 
# --- 1. FETCH MESSAGES (GET) ---
messages_data = []
try:
    # Your backend expects: /messages?empID=27
    response = requests.get(API_URL, params={"empID": current_emp_id})
    
    if response.status_code == 200:
        messages_data = response.json()
        # Sort by msgID so conversation flows naturally (Oldest -> Newest)
        messages_data.sort(key=lambda x: x.get('msgID', 0))
    else:
        st.error(f"Error loading messages: {response.status_code}")
except Exception as e:
    st.error(f"Connection Error: {e}")
 
# --- 2. DISPLAY CHAT HISTORY ---
# We iterate through the DB data instead of local session state
if messages_data:
    for msg in messages_data:
        msg_id = msg.get('msgID')
        content = msg.get('content')
        sender = msg.get('sender')
        
        # LOGIC: If I sent it -> align Right ("user"). If they sent it -> align Left ("assistant")
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
 
# --- 3. SEND NEW MESSAGE (POST) ---
if prompt := st.chat_input("Type your message..."):
    
    # Optimistic UI: Show the message immediately while processing
    with st.chat_message("user"):
        st.write(prompt)
    
    # Prepare Payload strictly according to your backend requirements
    payload = {
        "content": prompt,
        "sender": int(current_emp_id),
        "receiver": [int(recipient_id)] # Backend requires a LIST
    }
    
    try:
        res = requests.post(API_URL, json=payload)
        
        if res.status_code == 201:
            st.success("Sent!")
            # Rerun to fetch the new message from DB and confirm it was saved
            st.rerun()
        elif res.status_code == 404:
            st.error("Error: The Recipient or Sender ID does not exist.")
        else:
            st.error(f"Failed to send: {res.status_code}")
            st.write(res.text)
            
    except Exception as e:
        st.error(f"Connection failed: {e}")