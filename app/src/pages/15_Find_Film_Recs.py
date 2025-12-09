import streamlit as st
import requests
#import mysql.connector
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Find Film Recommendations")
st.write("")

# 1. Map Genre Names to IDs (These must match your DB IDs)
genre_map = {
    "Action": 1, "Rom-Com": 2, "Adventure": 3, "Animation": 4, 
    "Comedy": 5, "Documentary": 6, "Drama": 7, "Family": 8, 
    "Fantasy": 9, "Horror": 10, "Mystery": 11, "Romance": 12, 
    "Sci-Fi": 13, "Thriller": 14
}

genre_selection = st.selectbox(
    "Select a Genre",
    list(genre_map.keys())
)

# 2. Get the numeric ID from the selection
genre_id = genre_map[genre_selection]

st.write("# Getting you the top movies for your genre!")

if st.button("Get Movies"):
    # 3. Use an f-string to put the number into the URL
    # We keep 'http://api:4000' as requested
    url = f'http://api:4000/movie/genres/{genre_id}/movies'
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        movies_genres = response.json()
        st.dataframe(movies_genres)
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
