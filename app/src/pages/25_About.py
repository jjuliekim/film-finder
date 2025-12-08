import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
    This is FilmFinder, the all-in-one platform that allows you to find 
    films given an actors' name, watch them, and actually rate them out of five stars 
    and write detailed reviews. 
    
    Inspired by Netflix and Letterboxd, users can now view 
    cinema and rate what they watch all in one platform, instead of multiple platforms.
    Users can also host watchparties with friends and family remotely across
    continents and use Advanced Search to filter movies by duration, language, genre, 
    and actor.

    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")