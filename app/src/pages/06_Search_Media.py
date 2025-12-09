# the page for the annotations the analyst made on advanced serahced 

import streamlit as st
import pandas as pd
from datetime import datetime
from modules.nav import SideBarLinks

# 1. Navigation
SideBarLinks()

# 2. Page Configuration
st.title("Filter & Annotate")
st.caption("Define complex search filters and save them with analysis notes.")

if "saved_filters" not in st.session_state:
    st.session_state.saved_filters = []

st.subheader("1. Define Search Criteria")

with st.container(border=True):
    col1, col2 = st.columns(2)
    
    with col1:
        genre_input = st.selectbox("Genre", ["Any", "Action", "Comedy", "Drama", "Sci-Fi", "Horror"])
        actor_input = st.text_input("Actor (e.g. Tom Holland)")
    
    with col2:
        rating_input = st.selectbox("MPAA Rating", ["Any", "G", "PG", "PG-13", "R"])
        duration_input = st.slider("Max Duration (minutes)", 60, 240, 120)

    preview_text = f"**Current Filter:** Movies in '{genre_input}' genre"
    if actor_input:
        preview_text += f", starring '{actor_input}'"
    if rating_input != "Any":
        preview_text += f", rated '{rating_input}'"
    preview_text += f", under {duration_input} mins."
    
    st.info(preview_text)

st.subheader("2. Analyst Annotations")

annotation_text = st.text_area(
    "Why is this segment important?", 
    placeholder="Ex: This demographic shows high retention during summer holidays..."
)

if st.button("Save Filter Preset", type="primary"):
    if annotation_text:
        new_entry = {
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Filter Description": preview_text.replace("**Current Filter:** ", ""),
            "Genre": genre_input,
            "Actor": actor_input if actor_input else "All",
            "Rating": rating_input,
            "Max Duration": f"{duration_input} min",
            "Notes": annotation_text
        }
        
        st.session_state.saved_filters.append(new_entry)
        st.success("Filter saved successfully!")
    else:
        st.warning("Please add an annotation note before saving.")

st.markdown("---")

st.subheader("📂 Saved Filter Library")

if len(st.session_state.saved_filters) > 0:
    df = pd.DataFrame(st.session_state.saved_filters)
    
    cols = ["Date", "Filter Description", "Notes", "Genre", "Actor"]
    
    st.dataframe(
        df[cols], 
        use_container_width=True,
        hide_index=True,
        column_config={
            "Notes": st.column_config.TextColumn("Analyst Notes", width="large"),
            "Filter Description": st.column_config.TextColumn("Criteria Summary", width="medium"),
        }
    )
    
    if st.button("Clear All Saved Filters"):
        st.session_state.saved_filters = []
        st.rerun()

else:
    st.write("No saved filters yet. Use the form above to create one.")