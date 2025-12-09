import streamlit as st
from modules.nav import SideBarLinks


st.set_page_config(layout="wide")
SideBarLinks()

st.title("Add a Profile")

st.write("")


profile_type = st.selectbox(
    "Select Profile Type",
    ["Kids", "Teens", "Adults"]
)

profile_name = st.text_input("Enter Profile Name")

if st.button("Create Profile"):
    if profile_name.strip() == "":
        st.error("Please enter a profile name.")
    else:
        st.success(f"Profile **{profile_name}** ({profile_type}) created successfully!")




