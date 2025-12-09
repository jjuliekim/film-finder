import streamlit as st
from modules.nav import SideBarLinks
import random

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Watch Party")

st.write("")
st.write("### Start a Watch Party")


movie_name = st.text_input("Enter Movie Name")

party_id = random.randint(100000, 999999)
watchparty_link = f"https://filmfinder.com/watchparty/{party_id}"

# Movie section
st.write("### Movie")
st.write(movie_name)

# Watchparty link 
st.write("### Watchparty Link")

# Share invite Button
if st.button("Share Invite Link"):
    st.write("Copy this link and send it to your friends!")
    st.code(watchparty_link)

# Start the watchparty Button
if st.button("Start Watchparty"):
    st.success("Watchparty started!")
