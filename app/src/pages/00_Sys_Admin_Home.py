import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome System Admin, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Your Tasks', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/03_Tasks.py')

if st.button('View User Requests', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_User_Requests.py')

if st.button('View Version History of Film Finder', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_App_Vers_History.py')

if st.button('Check your messages with the team', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/04_Direct_Message.py')