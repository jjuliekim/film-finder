import streamlit as st
import mysql.connector
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Find Film Recommendations")
st.write("")

# xxx
genre = st.selectbox(
    "Select a Genre",
    [
        "Any",
        "Action", "Rom-Com", "Adventure", "Animation", "Comedy",
        "Documentary", "Drama", "Family", "Fantasy", "Horror",
        "Mystery", "Romance", "Sci-Fi", "Thriller",
    ]
)

# 
if st.button("Get Recommendations", type="primary"):

    try:
        # Connect to DB
        conn = mysql.connector.connect(
            host="localhost",       # change to your DB host
            user="your_username",   # DB username
            password="your_password",
            database="your_db_name"
        )
        cursor = conn.cursor(dictionary=True)

        # 
        query = """
            SELECT m.title, m.yearReleased, m.duration,
                   AVG(r.starRating) AS avgRating,
                   COUNT(r.reviewID) AS numReviews
            FROM Movies m
            JOIN Reviews r ON m.movieID = r.movieID
            GROUP BY m.movieID
        """

        # Duration filter
        if duration_filter == "Under 2 hours":
            query += " HAVING m.duration <= 120"
        elif duration_filter == "2 hours or more":
            query += " HAVING m.duration > 120"

        query += " ORDER BY avgRating DESC, numReviews DESC LIMIT 10;"

        cursor.execute(query)
        results = cursor.fetchall()

        if len(results) == 0:
            st.info("No films found.")
        else:
            st.success(f"Top {len(results)} films based on user reviews:")

            for movie in results:
                st.write(f"**{movie['title']}** ({movie['yearReleased']})")
                st.write(f"- Duration: {movie['duration']} mins")
                st.write(f"- Avg Rating: {movie['avgRating']:.2f} ⭐ ({movie['numReviews']} reviews)")
                st.write("---")

        cursor.close()
        conn.close()

    except Exception as e:
        st.error(f"Error connecting to database: {e}")
