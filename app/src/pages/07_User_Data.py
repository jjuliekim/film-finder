import streamlit as st
import pandas as pd
import plotly.express as px
from modules.nav import SideBarLinks
import requests
 
# Navigation
SideBarLinks()
 
st.markdown("## <span style='color:blue;'> Film Finder User Analytics </span>", unsafe_allow_html=True)
 
# KPI Section (Hardcoded)
st.subheader("Key Performance Indicators (for this week)")
 
col1, col2, col3 = st.columns(3)
 
with col1:
    st.metric(label="Total Registered Users", value="12,450", delta="15")
 
with col2:
    st.metric(label="Average Rating", value="4.15", delta="0.5")
 
with col3:
    st.metric(label="Average Session Time", value="85:03 mins", delta="-23:00")
 
st.markdown("---")

st.subheader("User Activity Inspector")
st.markdown("Enter a User ID to view their real-time Reviews and Lists from the database.")
 
user_input = st.number_input("Enter User ID", min_value=1, value=1, step=1)
search_btn = st.button("Fetch User Data")
 
BASE_API_URL = "http://api:4000/user"
 
if search_btn:
    try:
        tab1, tab2 = st.tabs(["User Reviews", "User Lists"])
        
        with tab1:
            st.markdown(f"### Reviews for User {user_input}")
            reviews_url = f"{BASE_API_URL}/reviews/users/{user_input}"
            response = requests.get(reviews_url)
            
            if response.status_code == 200:
                reviews_data = response.json()
                
                if reviews_data:
                    df_reviews = pd.DataFrame(reviews_data)
                    
                    if 'starRating' in df_reviews.columns:
                        ratings_counts = df_reviews['starRating'].value_counts().reset_index()
                        ratings_counts.columns = ['Rating', 'Count']
                        
                        fig_rating = px.pie(
                            ratings_counts,
                            names='Rating',
                            values='Count',
                            title=f"User {user_input}'s Rating Habits",
                            hole=0.4
                        )
                        st.plotly_chart(fig_rating, use_container_width=True)
                    
                    st.divider()

                    cols_to_show = ['reviewID', 'movieID', 'starRating', 'reviewText', 'publishedDate']
                    final_cols = [c for c in cols_to_show if c in df_reviews.columns]
                    st.dataframe(df_reviews[final_cols], use_container_width=True)
                    
                else:
                    st.info("No reviews found for this user.")
            else:
                st.error(f"Failed to fetch reviews. Server returned: {response.status_code}")
 
        with tab2:
            st.markdown(f"### Lists for User {user_input}")
            lists_url = f"{BASE_API_URL}/lists/users/{user_input}"
            response_lists = requests.get(lists_url)
            
            if response_lists.status_code == 200:
                lists_data = response_lists.json()
                if lists_data:
                    df_lists = pd.DataFrame(lists_data)
                    st.dataframe(df_lists, use_container_width=True)
                else:
                    st.info("No lists created by this user.")
            else:
                st.error(f"Failed to fetch lists. Server returned: {response_lists.status_code}")
 
    except Exception as e:
        st.error(f"Connection Error: {e}")
