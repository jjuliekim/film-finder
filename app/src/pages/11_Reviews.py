import streamlit as st
from modules.nav import SideBarLinks
import random

st.set_page_config(layout="wide")
SideBarLinks()

st.title("📝 My Film Reviews")
st.write("Write, view, and manage your film reviews with star ratings.")

# Initialize session state for reviews
if "my_reviews" not in st.session_state:
    # Each review: {"film": str, "review": str, "stars": int, "share_link": str}
    st.session_state.my_reviews = []

# -------------------------
# Add a new review
# -------------------------
st.write("### Write a New Review")
film_name = st.text_input("Film Title")
review_text = st.text_area("Your Review")
star_rating = st.number_input("Star Rating (1-5)", min_value=1, max_value=5, step=1)

if st.button("Submit Review"):
    if film_name.strip() == "" or review_text.strip() == "":
        st.error("Please enter both a film title and review text.")
    else:
        # Generate share link
        review_id = random.randint(100000, 999999)
        share_link = f"https://filmfinder.com/review/{review_id}"

        # Append to session state
        st.session_state.my_reviews.append({
            "film": film_name.strip(),
            "review": review_text.strip(),
            "stars": star_rating,
            "share_link": share_link
        })
        st.success(f"Review for '{film_name}' submitted!")

# -------------------------
# Display all reviews
# -------------------------
st.write("---")
st.write("### My Published Reviews")

if st.session_state.my_reviews:
    for i, review in enumerate(st.session_state.my_reviews):
        col1, col2, col3 = st.columns([6, 2, 1])
        with col1:
            st.write(f"**{review['film']}** ({review['stars']} ⭐)")
            st.write(f"{review['review']}")
        with col2:
            if st.button("Share Review", key=f"share_{i}"):
                st.info("Share this link with others:")
                st.code(review["share_link"])
        with col3:
            if st.button("Delete", key=f"del_{i}"):
                st.session_state.my_reviews.pop(i)
                st.success(f"Deleted review for '{review['film']}'")
else:
    st.write("_You have not published any reviews yet._")
