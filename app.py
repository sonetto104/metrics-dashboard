import streamlit as st

# Import page functions
from pages.process_data_page import process_data_page
from pages.visualise_data_page import visualise_data_page

# Set page title
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Process Data", "Visualise Data"])

# Navigate to the selected page
if page == "Process Data":
    process_data_page()
elif page == "Visualise Data":
    visualise_data_page()