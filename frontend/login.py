import streamlit as st
import requests
import json
def login_form():
    username = st.session_state["username"]
    password = st.session_state["login_password"]

    print(username , password)
    
    url = "http://127.0.0.1:8000/auth/token"

    
    payload = f'username={username}&password={password}'
    
    print(payload)
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
        }
 
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    
    return response

    
    
    