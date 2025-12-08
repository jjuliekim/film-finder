import streamlit as st
import requests

st.title("Advanced Movie Search")

with st.expander("Advanced Search Filters", expanded=False):
    col1, col2 = st.columns(2)

    # Left column
    with col1:
        language = st.selectbox(
            "Language",
            ["All", "English", "Spanish", "Mandarin", "German", "Arabic", "French"]
        )
        actor = st.text_input("Actor Name")
        director = st.text_input("Director Name")

    # Right column
    with col2:
        genre = st.selectbox(
            "Genre",
            [
                "Any",
                "Action", "Rom-Com", "Adventure", "Animation", "Comedy",
                "Documentary", "Drama", "Family", "Fantasy", "Horror",
                "Mystery", "Romance", "Sci-Fi", "Thriller",
            ]
        )

        duration_input = st.slider("Max Duration (minutes)", 60, 240, 120)

        min_rating = st.number_input(
            "Minimum User Rating (1-5)",
            min_value=1,
            max_value=5,
            value=1,
            step=1
        )

    show_trailers = st.checkbox("Show movies with trailers only")

    sort_by = st.selectbox(
        "Sort Results By",
        ["Title A–Z", "Title Z–A", "New Releases First", "Oldest First"]
    )

    apply_filters = st.button("Apply Filters")

#connect to api
params = {}

if apply_filters:
    # Language
    if language != "All":
        params["language"] = language

    # Genre
    if genre != "Any":
        params["genre"] = genre

    # Actor / Director
    if actor:
        params["actor"] = actor
    if director:
        params["director"] = director

    # Duration filter
    params["max_duration"] = duration_input

    # Minimum user rating
    params["min_rating"] = min_rating

    # Trailers only
    if show_trailers:
        params["has_trailer"] = True

    # Sorting
    params["sort_by"] = sort_by

    # Example: print parameters (replace with actual API request)
    st.write("Filters applied:")
    st.json(params)

    # Example API request:
    # response = requests.get("http://your-api/movies", params=params)
    # st.write(response.json())
