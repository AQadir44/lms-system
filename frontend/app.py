import streamlit as st
import requests
import json
from frontend.register import registration_form
from frontend.login import login_form


st.set_page_config(
  initial_sidebar_state = "collapsed",   
  page_title = "LMS",
  layout="wide" , 
)


home = st.sidebar.button("Home")
register = st.sidebar.button("SignUp")
contact = st.sidebar.button("Contact")


st.title("Welcome to LMS")

with st.form(key="login_form"):
    st.text_input("User Name" , key="username")
    st.text_input("Password" , key="login_password")

    st.form_submit_button(label="Submit" , on_click=login_form)

st.text("You don't have an account ?")
login_register = st.button("Sign Up")

if register or login_register:
    st.header("Register Form")

    with st.form(key="register_form"):
        st.text_input("First Name" , key="first_name")
        st.text_input("Last Name" , key="last_name")
        st.text_input("Email" , key="email")
        st.text_input("Country" , key="country")
        st.text_input("City" , key="city")
        st.text_input("Password" , key="password")

        st.form_submit_button(label="Submit" , on_click=registration_form)

    # if submit:
# st.write(first_name , last_name , email , country , city , password)

