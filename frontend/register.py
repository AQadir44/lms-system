import streamlit as st


def registration_form():

    first_name = st.session_state["first_name"]   
    last_name = st.session_state["last_name"]
    email = st.session_state["email"]
    country = st.session_state["country"]
    city = st.session_state["city"]
    password = st.session_state["password"]

    print(first_name , last_name , email , country , city , password)
    