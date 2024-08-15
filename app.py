import streamlit as st

# Import page functions
from pages.process_data_page import process_data_page
from pages.visualise_data_page import visualize_data_page

# Set page title
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Process Data", "Visualize Data"])

# Navigate to the selected page
if page == "Process Data":
    process_data_page()
elif page == "Visualize Data":
    visualize_data_page()