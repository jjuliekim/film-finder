import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Movie Enthusiast, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Get Film Recommendations', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/15_Find_Film_Recs.py')

if st.button('Create Kids Profile', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/19_Add_Kids_Prof.py') # brings to kids movie search

if st.button(
    "Start a Watch Party",
    type='primary',
    use_container_width=True):
    st.switch_page('pages/17_Watch_Party.py')

if st.button(
    "Advanced Film Search (Multiple Filters)",
    type='primary',
    use_container_width=True
):
    st.switch_page("pages/18_Advanced_Search.py")





