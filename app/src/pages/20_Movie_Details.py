import logging
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

logger = logging.getLogger(__name__)
SideBarLinks()

st.title("Search Movie Details")