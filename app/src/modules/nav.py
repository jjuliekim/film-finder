# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app
import os
import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/25_About.py", label="About", icon="🧠")


#### ------------------------ Role of system_administrator ------------------------
def SysAdminHomeNav():
    st.sidebar.page_link(
        "pages/00_Sys_Admin_Home.py", label="System Administrator Home", icon="👤"
    )


def AppVersHistory(): #user story 1.1 + 1.2 
    st.sidebar.page_link(
        "pages/01_App_Vers_History.py", label="App Version History", icon="📂"
    )


def UserRequests(): #user story 1.3
    st.sidebar.page_link("pages/02_User_Requests.py", label="Manage User Requests", icon="👥")

def Tasks(): #user story 1.4 + 1.5 
    st.sidebar.page_link("pages/03_Tasks.py", label="Tasks", icon="✅")

def DirectMessage(): #user story 1.6
    st.sidebar.page_link("pages/04_Direct_Message.py", label="Direct Messsage", icon="💬")



## ------------------------ Role of data_analyst ------------------------

def DataAnalystHomeNav():
    st.sidebar.page_link(
      "pages/05_Data_Analyst_Home.py", label="Data Analyst Home", icon="🏠"
    )

def SearchMediaNav(): #user story 2.1 
    st.sidebar.page_link("pages/06_Search_Media.py", label="Search Films/Saved Searches", icon="📁")

def UserData(): #user story 2.4
    st.sidebar.page_link("pages/07_User_Data.py", label="User Data", icon="💻")

def MovieAnalytics(): #user story 2.3 + 2.5
    st.sidebar.page_link("pages/08_Movie_Analytics.py", label="Movie Analytics", icon="📊")

def DirectMessage2(): #user story 2.6
    st.sidebar.page_link("pages/09_Direct_Message-2.py", label="Direct Message", icon="💬")






#### ------------------------ Movie Critic Role ------------------------
def MovieCriticHomeNav(): 
    st.sidebar.page_link("pages/10_Movie_Critic_Home.py", label="Movie Critic", icon="🎦")

def Reviews(): #user story 3.1 + 3.5
    st.sidebar.page_link("pages/11_Reviews.py", label="Reviews", icon="💬")
    #st.switch_page('pages/00_Pol_Strat.py') # change to end destination?? 

def WatchLists(): #user story 3.2 + 3.3
    st.sidebar.page_link("pages/12_Watch_Lists.py", label="My Watch Lists", icon="📋")

def MovieDetails():
    st.sidebar.page_link("pages/20_Movie_Details.py", label="Movie Search", icon="🎬")

def AdvancedSearch(): #user story 3.4
    st.sidebar.page_link("pages/18_Advanced_Search.py", label="Advanced Search", icon="🔎")

#### ------------------------ Bilingual Movie Enthusiast  ------------------------
def BilingualMEHomeNav(): 
    st.sidebar.page_link("pages/14_Bilingual_ME_Home.py", label="Bilingual Movie Enthusiast", icon="🍿")


def FindFilmRecs(): #user story 4.2
    st.sidebar.page_link("pages/15_Find_Film_Recs.py", label="Film Recommendations", icon="🪄")

def MoviesSearch(): #user story 4.3
    st.sidebar.page_link("pages/19_Kids_Prof.py", label="Add Profiles", icon="➕")

def WatchParty(): #user story 4.5
    st.sidebar.page_link("pages/17_Watch_Party.py", label="Host Watch Party", icon="👪")


def AdvancedSearch(): #user story 4.6
    st.sidebar.page_link("pages/18_Advanced_Search.py", label="Advanced Search", icon="🔎")

def AddKids(): #user story 4.6
    st.sidebar.page_link("pages/19_Kids_Prof.py", label="Add Profiles", icon="➕")

    # --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()
        AboutPageNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "system_administrator":
            SysAdminHomeNav()
            AppVersHistory()
            UserRequests()
            Tasks()
            DirectMessage()


        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "data_analyst":
            DataAnalystHomeNav()
            SearchMediaNav()
            UserData()
            MovieAnalytics()
            DirectMessage2()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "movie_critic":
            MovieCriticHomeNav()
            Reviews()
            WatchLists()
            MovieDetails()
            AdvancedSearch()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "bilingual_me":
            BilingualMEHomeNav()
            FindFilmRecs()
            WatchParty()
            AdvancedSearch()

