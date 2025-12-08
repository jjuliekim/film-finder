import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("🎬 Personal Film Lists") 
st.write("Manage your watched, to-watch, and rated movies easily.")

# Initialize session state for lists
if "film_lists" not in st.session_state:
    st.session_state.film_lists = {
        "Watched": [],
        "To Watch": [],
        "5-Star Rating": [],
        "Cozy": [],
        "Christmas Meet Cute": [],
    }

st.write("### Create a New Watchlist")
new_list_name = st.text_input("New Watchlist Name")
if st.button("Create Watchlist"):
    if new_list_name.strip() == "":
        st.error("Please enter a valid list name.")
    elif new_list_name in st.session_state.film_lists:
        st.error("A list with this name already exists.")
    else:
        st.session_state.film_lists[new_list_name] = []
        st.success(f"Watchlist **{new_list_name}** created!")

# Add a new film to list

st.write("### Add a Film to a List")
new_film = st.text_input("Film Title")
selected_list = st.selectbox("Select List", list(st.session_state.film_lists.keys()))

if st.button("Add Film"):
    if new_film.strip() == "":
        st.error("Please enter a film title.")
    else:
        st.session_state.film_lists[selected_list].append(new_film.strip())
        st.success(f"'{new_film}' added to **{selected_list}** list!")


# show curr lists

st.write("---")
st.write("### Your Film Lists")

for list_name, films in st.session_state.film_lists.items():
    st.write(f"**{list_name}**")
    if films:
        for i, film in enumerate(films):
            col1, col2, col3, col4 = st.columns([3, 1, 2, 1])
            with col1:
                st.write(f"- {film}")
            with col2:
                # Move film to another list
                move_to = st.selectbox(
                    f"Move '{film}' to:",
                    [ln for ln in st.session_state.film_lists.keys() if ln != list_name],
                    key=f"move_{list_name}_{i}"
                )
            with col3:
                if st.button(f"Move '{film}'", key=f"move_btn_{list_name}_{i}"):
                    # Move film
                    st.session_state.film_lists[list_name].remove(film)
                    st.session_state.film_lists[move_to].append(film)
                    st.experimental_rerun()
            with col4:
                if st.button(f"Delete", key=f"del_{list_name}_{i}"):
                    st.session_state.film_lists[list_name].remove(film)
                    st.experimental_rerun()
    else:
        st.write("No films in this list yet")



