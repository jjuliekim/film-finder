import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')
SideBarLinks()

st.title("🎬 Search Movie Details")

# Get all movies
try:
    movies_response = requests.get("http://api:4000/movie/movies")
    movies_response.raise_for_status()
    all_movies = movies_response.json()
    movie_options = {}
    for m in all_movies:
        display_name = f"{m['title']}"
        movie_options[display_name] = m['movieID']
except Exception as e:
    st.error(f"Error loading movies: {e}")
    movie_options = {}
    
# Movie selection
if movie_options:
    selected_movie = st.selectbox("Select a Movie", list(movie_options.keys()))
    movie_id = movie_options[selected_movie]
    
    if st.button("Get Movie Details"):
        try:
            # Get movie details
            movie_response = requests.get(f"http://api:4000/movie/movies/{movie_id}")
            movie_response.raise_for_status()
            movie = movie_response.json()
            
            st.write("---")
            st.write(f"## {movie.get('title')}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Year:** {movie.get('yearReleased')}")
            with col2:
                st.write(f"**Duration:** {movie.get('duration')} hours")
            with col3:
                st.write(f"**Movie ID:** {movie.get('movieID')}")
            
            st.write("---")
            
            # Get and display directors
            st.write("### Directors")
            try:
                directors_response = requests.get(f"http://api:4000/movie/movies/{movie_id}/directors")
                directors_response.raise_for_status()
                directors = directors_response.json()
                
                for director in directors:
                  st.write(f"- {director.get('firstName')} {director.get('lastName')}")
            except Exception as e:
                st.warning(f"Could not load directors: {e}")
            
            st.write("---")
            
            # Get and display actors
            st.write("### Actors")
            try:
                actors_response = requests.get(f"http://api:4000/movie/movies/{movie_id}/actors")
                actors_response.raise_for_status()
                actors = actors_response.json()
                num_cols = 3
                cols = st.columns(num_cols)
                for actor in actors:
                  st.write(f"- {actor.get('firstName')} {actor.get('lastName')}")
            except Exception as e:
                st.warning(f"Could not load actors: {e}")
  
            st.write("---")
            
            # Get and display captions
            st.write("### Available Captions")
            try:
                captions_response = requests.get(f"http://api:4000/movie/movies/{movie_id}/captions")
                captions_response.raise_for_status()
                captions = captions_response.json()
                
                if captions:
                    # Group captions by language
                    languages = set()
                    for caption in captions:
                        languages.add(caption.get('lang'))
                    
                    st.write(f"**Languages available:** {', '.join(languages)}")
                  
                else:
                    st.write("_No captions available_")
            except Exception as e:
                st.warning(f"Could not load captions: {e}")
            
        except Exception as e:
            st.error(f"Error loading movie details: {e}")
else:
    st.warning("No movies available to display.")