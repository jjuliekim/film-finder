import streamlit as st
import requests
#import mysql.connector
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

import streamlit as st
import requests
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

st.write("# Accessing a REST API from Within Streamlit")

if st.button("Get Movies"):
    # 3. Use an f-string to put the number into the URL
    # We keep 'http://api:4000' as requested
    url = f'http://api:4000/movie/genres/{genre_id}/movies'
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Check for errors
        movies_genres = response.json()
        st.dataframe(movies_genres)
    except Exception as e:
        st.error(f"Error connecting to API: {e}")




# st.title("Find Film Recommendations")
# st.write("")

# # xxx
# genre = st.selectbox(
#     "Select a Genre",
#     [
#         "Any",
#         "Action", "Rom-Com", "Adventure", "Animation", "Comedy",
#         "Documentary", "Drama", "Family", "Fantasy", "Horror",
#         "Mystery", "Romance", "Sci-Fi", "Thriller",
#     ]
# )


# st.write("# Accessing a REST API from Within Streamlit")

# movies_genres = requests.get('http://api:4000/movie/genres/<int:genre_id>/movies').json()
# try:
#   st.dataframe(movies_genres) 
# except:
#   st.write("Could not connect to database to get the movies!")


# """
# Simply retrieving data from a REST api running in a separate Docker Container.

# If the container isn't running, this will be very unhappy.  But the Streamlit app 
# should not totally die. 
# """

# data = {} 
# try:
#   data = requests.get('http://web-api:4000/data').json()
# except:
#   st.write("**Important**: Could not connect to sample api, so using dummy data.")
#   data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

# st.dataframe(data)



# 
# if st.button("Get Recommendations", type="primary"):

#     try:
#         # Connect to DB
#         conn = mysql.connector.connect(
#             host="localhost",       # change to your DB host
#             user="your_username",   # DB username
#             password="your_password",
#             database="your_db_name"
#         )
#         cursor = conn.cursor(dictionary=True)

#         # 
#         query = """
#             SELECT m.title, m.yearReleased, m.duration,
#                    AVG(r.starRating) AS avgRating,
#                    COUNT(r.reviewID) AS numReviews
#             FROM Movies m
#             JOIN Reviews r ON m.movieID = r.movieID
#             GROUP BY m.movieID
#         """

#         # Duration filter
#         if duration_filter == "Under 2 hours":
#             query += " HAVING m.duration <= 120"
#         elif duration_filter == "2 hours or more":
#             query += " HAVING m.duration > 120"

#         query += " ORDER BY avgRating DESC, numReviews DESC LIMIT 10;"

#         cursor.execute(query)
#         results = cursor.fetchall()

#         if len(results) == 0:
#             st.info("No films found.")
#         else:
#             st.success(f"Top {len(results)} films based on user reviews:")

#             for movie in results:
#                 st.write(f"**{movie['title']}** ({movie['yearReleased']})")
#                 st.write(f"- Duration: {movie['duration']} mins")
#                 st.write(f"- Avg Rating: {movie['avgRating']:.2f} ⭐ ({movie['numReviews']} reviews)")
#                 st.write("---")

#         cursor.close()
#         conn.close()

#     except Exception as e:
#         st.error(f"Error connecting to database: {e}")
