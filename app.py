import streamlit as st
import pdfplumber
import PyPDF2
import pandas as pd
from helper_functions import extract_date_from_pdf, anonymize_apprentice_names

st.title("PDF Metrics Analysis")

uploaded_file = st.file_uploader("Upload a PDF file", type=['pdf'])

if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        # Extract PDF date and tables
        pdf_date = extract_date_from_pdf(uploaded_file)
        tables = [page.extract_table() for page in pdf.pages]