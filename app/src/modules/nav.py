# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

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

def DirectMessage(): #user story 2.6
    st.sidebar.page_link("pages/09_Direct_Message.py", label="Direct Messsage", icon="💬")






#### ------------------------ Movie Critic Role ------------------------
def MovieCriticHomeNav(): 
    st.sidebar.page_link("pages/10_Movie_Critic_Home.py", label="Movie Critic", icon="🎦")

def Reviews(): #user story 3.1 + 3.5
    st.sidebar.page_link("pages/11_Reviews.py", label="Reviews", icon="💬")
    #st.switch_page('pages/00_Pol_Strat.py') # change to end destination?? 

def WatchLists(): #user story 3.2 + 3.3
    st.sidebar.page_link("pages/12_Watch_Lists.py", label="My Watch Lists", icon="📋")


def MoviesSearch(): #user story 3.4 + 3.6
    st.sidebar.page_link("pages/13_Movies_Search.py", label="Advanced Search", icon="🔎")

#### ------------------------ Bilingual Movie Enthusiast  ------------------------
def BilingualMEHomeNav(): 
    st.sidebar.page_link("pages/14_Bilingual_ME_Home.py", label="Bilingual Movie Enthusiast", icon="🍿")

def Captions(): #user story 4.1
    st.sidebar.page_link("pages/02_Map_Demo.py", label="Captions", icon="🪄")

def FindFilmRecs(): #user story 4.2
    st.sidebar.page_link("pages/15_Find_Film_Recs.py", label="Film Recommendations", icon="🪄")

def MoviesSearch(): #user story 4.3
    st.sidebar.page_link("pages/16_Movies_Search.py", label="Add Profiles", icon="➕")

def WatchTrailer(): #user story 4.4
    st.sidebar.page_link("pages/02_Map_Demo.py", label="Watch Trailers", icon="📺")

def WatchParty(): #user story 4.5
    st.sidebar.page_link("pages/17_Watch_Party.py", label="Host Watch Party", icon="👪")


def AdvancedSearch(): #user story 4.6
    st.sidebar.page_link("pages/18_Advanced_Search.py", label="Advanced Search", icon="🔎")
