import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Personal Film Lists")
st.write("Manage your watched, to-watch, and rated movies easily.")

user_id = st.session_state["userID"]

st.write("### Create a New Watchlist")
new_list_name = st.text_input("New Watchlist Name")
if st.button("Create Watchlist"):
    if new_list_name.strip() == "":
        st.error("Please enter a list name.")
    else:
        try:
            list_data = {"userID": user_id, "listName": new_list_name.strip()}
            response = requests.post("http://api:4000/user/lists", json=list_data)
            response.raise_for_status()
            st.success(f"Watchlist **{new_list_name}** created!")
            st.rerun()
        except Exception as e:
            st.error(f"Error creating list: {e}")

# Add movie to list
# Get all movies
try:
    movies_response = requests.get('http://api:4000/movie/movies')
    movies_response.raise_for_status()
    all_movies = movies_response.json()
    movie_options = {}
    for m in all_movies:
        movie_options[m['title']] = m['movieID']
except Exception as e:
    st.error(f"Error loading movies: {e}")
    movie_options = {}
# Get user's lists
try:
    lists_response = requests.get(f"http://api:4000/user/lists/users/{user_id}")
    lists_response.raise_for_status()
    user_lists = lists_response.json()
except Exception as e:
    st.error(f"Error loading lists: {e}")
    user_lists = []

# Display entries    
if user_lists and movie_options:
    selected_movie = st.selectbox("Select Film", list(movie_options.keys()))
    movie_id = movie_options[selected_movie]
    
    list_options = {}
    for lst in user_lists:
        list_options[lst['listName']] = lst['listID']
    
    selected_list = st.selectbox("Select List", list(list_options.keys()))
    list_id = list_options[selected_list]

    if st.button("Add Film to List"):
        try:
            movie_data = {"movieID": movie_id}
            response = requests.post(f'http://api:4000/user/lists/{list_id}/movies', json=movie_data)
            response.raise_for_status()
            st.success(f"'{selected_movie}' added to **{selected_list}**!")
            st.rerun()
        except Exception as e:
            st.error(f"Error adding film: {e}")

# Display user's lists
st.write("---")
st.write("### Your Film Lists")

if user_lists:
    for user_list in user_lists:
        list_id = user_list["listID"]
        list_name = user_list["listName"]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{list_name}**")
        with col2:
            if st.button(f"Delete List", key=f"del_list_{list_id}"):
                try:
                    del_response = requests.delete(
                        f"http://api:4000/user/lists/{list_id}"
                    )
                    del_response.raise_for_status()
                    st.success(f"List **{list_name}** deleted!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting list: {e}")
                    
        try:
            list_movies_response = requests.get(f"http://api:4000/user/lists/{list_id}/movies")
            list_movies_response.raise_for_status()
            list_movies = list_movies_response.json()
        
            if list_movies:
                for movie in list_movies:
                    col_movie1, col_movie2 = st.columns([4, 1])
                    with col_movie1:
                        st.write(f"  - {movie['title']}")
                    with col_movie2:
                        if st.button("Remove", key=f"remove_{list_id}_{movie['movieID']}"):
                            try:
                                remove_response = requests.delete(
                                    f"http://api:4000/user/lists/{list_id}/movies/{movie['movieID']}"
                                )
                                remove_response.raise_for_status()
                                st.success(f"Removed '{movie['title']}'!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error removing movie: {e}")
        except Exception as e:
            st.error(f"Error loading movies for list {list_name}: {e}")
else:
  st.write("No watchlists yet. Create one above!")
