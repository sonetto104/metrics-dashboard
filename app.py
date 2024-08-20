import streamlit as st

# Import page functions
from pages_renamed.process_data_page import process_data_page
from pages_renamed.visualise_data_page import visualise_data_page

def main():
    # Create a sidebar with radio buttons for navigation
    page = st.sidebar.radio("Select a page:", ["Process Data", "Visualise Data"])

    # Navigate to the selected page
    if page == "Process Data":
        process_data_page()
    elif page == "Visualise Data":
        visualise_data_page()

if __name__ == "__main__":
    main()