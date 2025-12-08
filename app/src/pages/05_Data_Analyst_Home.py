import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Data Analyst, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('See Annotation on Saved Searches', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/06_Search_Media.py')

if st.button('View User Data & Analysis', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/07_User_Data.py')

if st.button('View Movie Data & Analysis', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_App_Vers_History.py')

if st.button('Check your messages with the team', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/09_Direct_Message-2.py')