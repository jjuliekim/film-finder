import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Find Film Recommendations")
st.write("")

# -------------------------------
# 1. Fetch genres with movie counts
# -------------------------------
@st.cache_data
def fetch_genres():
    try:
        url = "http://api:4000/genre/{genre_id}/movies"  
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Could not load genres: {e}")
        return []

genres = fetch_genres()

if genres:
    # Convert to DataFrame for plotting
    df_genres = pd.DataFrame(genres)
    df_genres = df_genres.rename(columns={"genreName": "Genre", "movie_count": "Count"})

    # -------------------------------
    # 2. Plot Bar Chart
    # -------------------------------
    st.subheader("Movie Count by Genre")
    fig = px.bar(
        df_genres,
        x="Genre",
        y="Count",
        title="Total Movies Available by Genre",
        color="Count",
        color_continuous_scale="Blues",
        text="Count"
    )
    fig.update_layout(xaxis_title="Genre", yaxis_title="Number of Movies")
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # 3. Genre Dropdown to fetch movies
    # -------------------------------
    genre_map = {g["genreName"]: g["genreID"] for g in genres}
    genre_options = [f"{g['genreName']} ({g['movie_count']})" for g in genres]

    genre_selection = st.selectbox(
        "Select a Genre to View Movies",
        genre_options
    )
    selected_genre_name = genre_selection.split(" (")[0]
    genre_id = genre_map[selected_genre_name]

    st.write(f"# Movies in {selected_genre_name}")

    if st.button("Get Movies"):
        #/movie/movies?year=2016&genre=Action&duration=2
        url = f'http://api:4000/movie/movies?genre={genre_selection}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            movies_genres = response.json()
            if movies_genres:
                st.success(f"Found {len(movies_genres)} movies in {selected_genre_name}")
                st.dataframe(movies_genres)
            else:
                st.warning(f"No movies found in {selected_genre_name}")
        except Exception as e:
            st.error(f"Error connecting to API: {e}") 
else:
    st.warning("No genre data available.")





# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from modules.nav import SideBarLinks

# # 1. Navigation
# SideBarLinks()

# # 2. Page Header
# st.markdown("## <span style='color:blue;'> Film Finder Movie Analytics </span>", unsafe_allow_html=True)

# # 3. KPI Section (Hardcoded)
# st.subheader("Content Performance")

# # Create 4 columns for the requested KPIs
# col1, col2 = st.columns(2)

# with col1:
#     st.metric(label="Top Genre", value="Action")

# with col2:
#     st.metric(label="Avg. Movie Length", value="1h 54m")

# col3, col4 = st.columns(2)

# with col3:
#     st.metric(label="Most Watched Actor", value="Tom Cruise")

# with col4:
#     st.metric(label="Top Director", value="Christopher Nolan")

# st.markdown("---")

# # 4. Chart Section (Mock Data)
# # Since you mentioned movies have genres, let's visualize the "Inventory by Genre"
# st.subheader("Movie Catalog Distribution by Genre")

# # Mock Data
# data = {
#     'Genre': ['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Horror', 'Animation', 'Thriller'],
#     'Count': [320, 210, 245, 180, 95, 150, 110]
# }
# df_movies = pd.DataFrame(data)

# # Create a Bar Chart
# fig = px.bar(
#     df_movies, 
#     x='Genre', 
#     y='Count', 
#     title='Total Movies Available by Genre',
#     color='Count',                 
#     color_continuous_scale='Blues', 
#     text='Count'                   
# )

# # Customize layout
# fig.update_layout(xaxis_title="Genre", yaxis_title="Number of Movies")

# # Display the chart
# st.plotly_chart(fig, use_container_width=True)
