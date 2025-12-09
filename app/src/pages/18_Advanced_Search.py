import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Advanced Movie Search")

# Get all directors
try:
    directors_response = requests.get("http://api:4000/movie/directors")
    directors_response.raise_for_status()
    all_directors = directors_response.json()
    director_options = ["All"] + [f"{d['firstName']} {d['lastName']}" for d in all_directors]
    director_map = {f"{d['firstName']} {d['lastName']}": d['directorID'] for d in all_directors}
except Exception as e:
    st.error(f"Error loading directors: {e}")
    director_options = ["All"]
    director_map = {}

# Search filters
with st.expander("Advanced Search Filters", expanded=False):
    col1, col2 = st.columns(2)

    # Left column
    with col1:
        captions = st.selectbox(
            "Captions",
            ["Any", "English", "Spanish", "Mandarin", "German", "Arabic", "French"]
        )
        
        director = st.selectbox("Director", director_options)

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

        duration_input = st.slider("Max Duration (hours)", 1, 3, 2)

        min_rating = st.number_input(
            "Minimum User Rating (1-5)",
            min_value=1,
            max_value=5,
            value=1,
            step=1
        )

    show_trailers = st.checkbox("Show movies with trailers only")

    apply_filters = st.button("Apply Filters")


# Connect to api
if apply_filters:
    params = {}
    
    # Genre
    if genre != "Any":
        params["genre"] = genre
    
    # Duration
    params["duration"] = duration_input
    
    # Get movies from api with filters
    try:
      response = requests.get("http://api:4000/movie/movies", params=params)
      response.raise_for_status()
      movies = response.json()
      
      # Director
      if director != "All":
        director_id = director_map.get(director)
        if director_id:
          try:
            director_movies_response = requests.get(f"http://api:4000/movie/directors/{director_id}/movies")
            director_movies_response.raise_for_status()
            director_movies = director_movies_response.json()
            director_movie_ids = [m['movieID'] for m in director_movies]
            movies = [m for m in movies if m['movieID'] in director_movie_ids]
          except Exception as e:
            st.warning(f"Could not filter by director: {e}")
      
      # Captions
      if captions != "Any":
        caption_filtered = []
        for movie in movies:
          try:
            captions_response = requests.get(f"http://api:4000/movie/movies/{movie['movieID']}/captions")
            captions_response.raise_for_status()
            captions_data = captions_response.json()
                
            for caption in captions_data:
              if caption.get('lang') == captions:
                caption_filtered.append(movie)
                break
          except:
              pass
          movies = caption_filtered
          
      # Rating
      if min_rating > 1:
        ratings = []
        for movie in movies:
            try:
                rating_response = requests.get(f"http://api:4000/user/reviews/movies/{movie['movieID']}")
                rating_response.raise_for_status()
                rating_data = rating_response.json()
                if rating_data:
                  avg_rating = sum(r['starRating'] for r in rating_data) / len(rating_data)
                  if avg_rating >= min_rating:
                    ratings.append(movie)
            except Exception as e:
                st.warning(f"Could not fetch rating for movie {movie['movieID']}: {e}") 
        movies = ratings
      
      # Trailers
      if show_trailers:
        trailer_filtered = []
        for movie in movies:
          try:
              trailers_response = requests.get(f"http://api:4000/movie/movies/{movie['movieID']}/trailers")
              trailers_response.raise_for_status()
              trailers = trailers_response.json()
                    
              if trailers:
                  trailer_filtered.append(movie)
          except:
              pass
        movies = trailer_filtered
        
      # Display results
      st.write("---")
      st.write(f"### Found {len(movies)} movies")
        
      if movies:
        for movie in movies:
          col_title, col_year, col_duration = st.columns([3, 1, 1])
                
          with col_title:
            st.write(f"**{movie.get('title')}**")
          with col_year:
            st.write(f"Year: {movie.get('yearReleased')}")
          with col_duration:
            st.write(f"Duration: {movie.get('duration')} hrs")
                
          st.write("---")
      else:
        st.info("No movies found matching your criteria.")
      
    except Exception as e:
        st.error(f"Error fetching movies: {e}")
        movies = []
