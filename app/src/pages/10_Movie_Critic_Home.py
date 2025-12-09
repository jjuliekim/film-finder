import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Movie Critic, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Write Review',  
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Reviews.py')

if st.button('My Watchlists', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Watch_Lists.py')

if st.button(
    "Movie Search",     
    type='primary',
    use_container_width=True):
    st.switch_page('pages/20_Movie_Details.py')

if st.button(
    "Advanced Film Search (Multiple Filters)",
    type='primary',
    use_container_width=True
):
    st.switch_page("pages/18_Advanced_Search.py")





