import streamlit as st
import requests

from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Find Film Recommendations")
st.write("")

genre_map = {
    "Mystery": 1,
    "Comedy": 2,
    "Crime": 3,
    "Thriller": 4,
    "Drama": 5,
    "Romance": 6,
    "Action": 7,
    "Children": 8,
    "Fantasy": 9,
    "Horror": 10,
    "Sci-Fi": 11,
    "Adventure": 12,
    "Documentary": 13,
    "Animation": 14,
    "War": 15,
    "Tragedy": 16,
    "Feel-Good": 17,
    "Teen": 18,
    "Coming of Age": 19,
    "High School": 20,
    "Historical": 21,
    "Romantic Comedy": 22,
    "Action-Horror": 23,
    "Musical": 24,
    "Horror-Thriller": 25,
}

genre_selection = st.selectbox("Select a Genre", list(genre_map.keys()))

genre_id = genre_map[genre_selection]

st.write("# Getting you the top movies for your genre!")

if st.button("Get Movies"):
    url = f"http://api:4000/movie/genres/{genre_id}/movies"

    try:
        response = requests.get(url)
        response.raise_for_status()
        movies_genres = response.json()
        st.dataframe(movies_genres)
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
