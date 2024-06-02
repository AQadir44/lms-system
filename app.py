import streamlit as st

def registration_form():

    first_name = st.session_state["first_name"]   
    last_name = st.session_state["last_name"]
    email = st.session_state["email"]
    country = st.session_state["country"]
    city = st.session_state["city"]
    password = st.session_state["password"]

    print(first_name , last_name , email , country , city , password)

st.set_page_config(
  initial_sidebar_state = "collapsed",   
  page_title = "LMS",
  layout="wide" , 
)

st.title("Welcome to LMS")

home = st.sidebar.button("Home")
login = st.sidebar.button("Login")
register = st.sidebar.button("SignUp")
contact = st.sidebar.button("Contact")

if login:
    st.write("Login")

if register:
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

