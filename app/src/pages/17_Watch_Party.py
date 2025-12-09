import streamlit as st
import requests
from datetime import date
import random

st.set_page_config(layout="wide")
st.title("Watch Party")

st.write("### Start a Watch Party")


# Step 1: Get movie list from backend
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


option = st.selectbox(
    "Choose a movie",
    [movie["title"] for movie in movies],
)

st.write("You selected:", option)


# # Convert movie data into dropdown format
# movie_options = {movie["Title"]: movie["movieID"] for movie in movies}

# selected_title = st.selectbox("Choose a Movie", list(movie_options.keys()))

party_date = st.date_input("Party Date", value=date.today())

party_id = random.randint(100000, 999999)
watchparty_link = f"https://filmfinder.com/watchparty/{party_id}"

# Start watch party
if st.button("Start Watch Party"):

    movie_id = movies[option]

    payload = {
        "movieID": movie_id,
        "partyDate": str(party_date),
        "userIDs": [1]   
    }

    try:
        url = "http://api:4000/watchparties"
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        party_id = data["party_id"]
        link = f"https://filmfinder.com/watchparty/{party_id}"

        st.success("Watch Party Created!")
        st.write("### Share this link:")
        st.code(link)

    except Exception as e:
        st.error(f"Error creating watch party: {e}")

    



# import streamlit as st
# from modules.nav import SideBarLinks
# import random

# st.set_page_config(layout="wide")
# SideBarLinks()

# st.title("Watch Party")

# st.write("")
# st.write("### Start a Watch Party")


# movie_name = st.text_input("Enter Movie Name")

# party_id = random.randint(100000, 999999)
# watchparty_link = f"https://filmfinder.com/watchparty/{party_id}"

# # Movie section
# st.write("### Movie")
# st.write(movie_name)

# # Watchparty link 
# st.write("### Watchparty Link")
# st.code(watchparty_link)

# # Share invite Button
# if st.button("Share Invite Link"):
#     st.write("Copy this link and send it to your friends!")
#     st.code(watchparty_link)

# # Start the watchparty Button
# if st.button("Start Watchparty"):
#     st.success("Watchparty started!")
