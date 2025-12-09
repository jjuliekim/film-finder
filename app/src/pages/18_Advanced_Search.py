import streamlit as st
import requests

st.set_page_config(layout="wide")
st.title("Advanced Movie Search")


@st.cache_data
def fetch_movies():
    try:
        url = "http://api:4000/movie/movies"
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Could not load movies: {e}")
        return []

movies = fetch_movies()

movie_options = ["Any"] + [movie["title"] for movie in movies]
movie_map = {movie["title"]: movie["movieID"] for movie in movies}


# Advanced Search Filters 

with st.expander("Advanced Search Filters", expanded=False):
    col1, col2 = st.columns(2)

    # Left column
    with col1:
        language = st.selectbox(
            "Language",
            ["All", "English", "Spanish", "Mandarin", "German", "Arabic", "French"]
        )
        actor = st.text_input("Actor Name")
        director_input = st.text_input("Director Name")
        selected_movie = st.selectbox(
            "Movie",
            movie_options
        )

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


params = {}
if apply_filters:
    if language != "All":
        params["language"] = language
    if genre != "Any":
        params["genre"] = genre
    if actor:
        params["actor"] = actor
    if director_input:
        params["director"] = director_input
    if selected_movie != "Any":
        params["movie_id"] = movie_map[selected_movie]

    params["max_duration"] = duration_input
    params["min_rating"] = min_rating
    if show_trailers:
        params["has_trailer"] = True
    params["sort_by"] = sort_by

    st.write("Filters applied:")
    st.json(params)

# get directors
if selected_movie != "Any" and st.button("Get Directors"):
    movie_id = movie_map[selected_movie]
    try:
        url = f"http://api:4000/movie/movies/{movie_id}/directors"
        response = requests.get(url)
        response.raise_for_status()
        directors = response.json()
        st.success(f"Directors for: {selected_movie}")
        st.json(directors)
    except Exception as e:
        st.error(f"Error connecting to API: {e}")


# Director dropdown based on selected movie

director_options = []

if selected_movie != "Any":
    movie_id = movie_map[selected_movie]
    try:
        url = f"http://api:4000/movies/movies/{movie_id}/directors"
        response = requests.get(url)
        response.raise_for_status()
        directors_list = response.json()

        # Format for selectbox
        director_options = ["Any"] + [
            f"{d['firstName']} {d['lastName']}" for d in directors_list
        ]

    except Exception as e:
        st.error(f"Error fetching directors for selected movie: {e}")
        director_options = ["Any"]

# Replace the previous director_input text box with a selectbox
if director_options:
    director_input = st.selectbox("Director", director_options)
else:
    director_input = "Any"








# import streamlit as st 
# import requests


# st.title("Advanced Movie Search")

# with st.expander("Advanced Search Filters", expanded=False):
#     col1, col2 = st.columns(2)

#     # Left column
#     with col1:
#         language = st.selectbox(
#             "Language",
#             ["All", "English", "Spanish", "Mandarin", "German", "Arabic", "French"]
#         )
#         actor = st.text_input("Actor Name")
#         director = st.text_input("Director Name")

#     # Right column
#     with col2:
#         genre = st.selectbox(
#             "Genre",
#             [
#                 "Any",
#                 "Action", "Rom-Com", "Adventure", "Animation", "Comedy",
#                 "Documentary", "Drama", "Family", "Fantasy", "Horror",
#                 "Mystery", "Romance", "Sci-Fi", "Thriller",
#             ]
#         )

#         duration_input = st.slider("Max Duration (minutes)", 60, 240, 120)

#         min_rating = st.number_input(
#             "Minimum User Rating (1-5)",
#             min_value=1,
#             max_value=5,
#             value=1,
#             step=1
#         )

#     show_trailers = st.checkbox("Show movies with trailers only")

#     sort_by = st.selectbox(
#         "Sort Results By",
#         ["Title A–Z", "Title Z–A", "New Releases First", "Oldest First"]
#     )

#     apply_filters = st.button("Apply Filters")

# #connect to api
# params = {}

# if apply_filters:
#     # Language
#     if language != "All":
#         params["language"] = language

#     # Genre
#     if genre != "Any":
#         params["genre"] = genre

#     # Actor and director
#     if actor:
#         params["actor"] = actor
#     # if director:
#     #     params["director"] = director

#     if director:
#         params["director"] = director
       
#         try:
           
#             directors_url = "http://api:4000/movies/directors"
#             response = requests.get(directors_url)
#             response.raise_for_status()
#             directors_list = response.json()

#             # Check if entered director exists
#             matched = [
#                 f"{d['firstName']} {d['lastName']}" 
#                 for d in directors_list 
#                 if director.lower() in (d['firstName'] + " " + d['lastName']).lower()
#             ]

#             if matched:
#                 st.write("Matching director(s) found in DB:")
#                 st.json(matched)
#             else:
#                 st.warning("Director not found in database.")

#         except Exception as e:
#             st.error(f"Error connecting to API: {e}")

#     # Duration info
#     params["max_duration"] = duration_input

#     # rating
#     params["min_rating"] = min_rating

#     # Trailers only checkbox
#     if show_trailers:
#         params["has_trailer"] = True

#     # Sorting it all 
#     params["sort_by"] = sort_by

#     # Example: print parameters (replace with actual API request)
#     st.write("Filters applied:")
#     st.json(params)




