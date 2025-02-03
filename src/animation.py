import json 
import requests
import streamlit as st
from streamlit_lottie import st_lottie

# Function to load and display the Lottie animation
def animation_Car():
    url = requests.get("https://assets2.lottiefiles.com/packages/lf20_mDnmhAgZkb.json") 
    url_json = {}

    # Check if the request was successful
    if url.status_code == 200:
        url_json = url.json()
    else:
        st.error("Error in URL")

    # Display the Lottie animation
    st_lottie(
        url_json,
        reverse=True,  # Reverse the direction of our animation
        height=400,    # Height of animation
        width=400,     # Width of animation
        speed=1,       # Speed of animation
        loop=True,     # Animation will run in a loop
        quality='high',  # Quality of the animation
        key='Car'      # Unique identifier for the animation
    )


