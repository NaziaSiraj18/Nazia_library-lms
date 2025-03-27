import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import plotly.express as px
import requests
from streamlit_lottie import st_lottie

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Lottie Animation
@st.cache_data
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_animation = load_lottie_url("https://assets10.lottiefiles.com/private_files/lf30_tlsgogek.json")

# Function to Load Library Data Safely
def load_library():
    try:
        with open("library.json", "r") as file:
            data = json.load(file)
            # Fix invalid timestamps
            for book in data:
                try:
                    datetime.strptime(book["added_data"], "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    book["added_data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Load Data
library = load_library()

# Convert JSON to DataFrame
if library:
    df = pd.DataFrame(library)
else:
    df = pd.DataFrame(columns=["title", "author", "publication_year", "genre", "read_status", "added_data"])

# App Header
st.markdown("<h1 class='main-header'>📚 Personal Library Manager</h1>", unsafe_allow_html=True)
if lottie_animation:
    st_lottie(lottie_animation, height=200, key="library_anim")

# Sidebar Filters
st.sidebar.header("Filters")
selected_genre = st.sidebar.selectbox("Select Genre", ["All"] + list(df["genre"].unique()))
read_status = st.sidebar.radio("Read Status", ["All", "Read", "Unread"])

# Apply Filters
if selected_genre != "All":
    df = df[df["genre"] == selected_genre]
if read_status == "Read":
    df = df[df["read_status"] == True]
elif read_status == "Unread":
    df = df[df["read_status"] == False]

# Display Books
st.write("### 📖 Your Book Collection")
st.dataframe(df, use_container_width=True)

# Visualization
if not df.empty:
    fig = px.histogram(df, x="publication_year", title="Books by Publication Year", nbins=15)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No books found in the selected category.")

st.success("✅ Personal Library Manager Loaded Successfully!")
