import requests
import streamlit as st
from modules.nav import SideBarLinks
import random

st.set_page_config(layout="wide")
SideBarLinks()

st.title("📝 My Film Reviews")
st.write("Write, view, and manage your film reviews with star ratings.")

if "my_reviews" not in st.session_state:
    st.session_state.my_reviews = []
user_id = st.session_state['userID']

st.write("### Write a New Review")
try:
    movies_response = requests.get('http://api:4000/movie/movies')
    movies_response.raise_for_status()
    movies = movies_response.json()
    movie_options = {f"{m['title']} ({m.get('yearReleased')})": m['movieID'] for m in movies}
except Exception as e:
    st.error(f"Error loading movies: {e}")
    movie_options = {}
selected_movie = st.selectbox("Select a Film", list(movie_options.keys()))
movie_id = movie_options[selected_movie]
review_text = st.text_area("Your Review")
star_rating = st.number_input("Star Rating (1-5)", min_value=1, max_value=5, step=1)

if st.button("Submit Review"):
    if not movie_id:
        st.error("Please select a movie.")
    elif review_text.strip() == "":
        st.error("Please enter a review.")
    else:
        review_data = {
          "userID": user_id, 
          "movieID": movie_id,
          "reviewText": review_text.strip(),
          "starRating": star_rating
        }
        response = requests.post('http://api:4000/user/reviews', json=review_data)
        response.raise_for_status()
        st.success("Review saved!")
        st.rerun()

st.write("---")
st.write("### My Published Reviews")

reviews_response = requests.get(f'http://api:4000/user/reviews/users/{user_id}')
reviews_response.raise_for_status()
user_reviews = reviews_response.json()
    
if user_reviews:
    for review in user_reviews:
        col1, col2 = st.columns([6, 2])
        try:
            movie_response = requests.get(f'http://api:4000/movie/movies/{review["movieID"]}')
            movie_response.raise_for_status()
            movie_data = movie_response.json()
            movie_title = movie_data.get('title')
            year = movie_data.get('yearReleased')
            display_title = f"{movie_title} ({year})"
        except:
            display_title = f"Movie ID: {review['movieID']}"
            
        with col1:
            st.write(f"**{display_title}** ({review['starRating']} ⭐)")
            st.write(f"{review['reviewText']}")
        with col2:
            if st.button("Delete", key=f"del_{review['reviewID']}"):
                try:
                  delete_response = requests.delete(f'http://api:4000/user/reviews/{review["reviewID"]}')
                  delete_response.raise_for_status()
                  st.success(f"Deleted review for '{display_title}'")
                  st.rerun()
                except Exception as e:
                  st.error(f"Error deleting review: {e}")
else:
    st.write("_You have not published any reviews yet._")
