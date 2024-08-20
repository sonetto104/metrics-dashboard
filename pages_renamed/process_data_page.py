import streamlit as st
import pdfplumber
from pathlib import Path
import pandas as pd
from helper_functions import extract_date_from_pdf, anonymise_apprentice_names
import base64

def process_data_page():
    st.title("Upload your metrics pdf here. All data will be anonymised.")

    # Add a radio button to select the data category (Individual, Team, Department)
    data_category = st.radio("Select Data Category:", ["Individual", "Programme", "Department"])

    uploaded_file = st.file_uploader("Upload a PDF file", type=['pdf'])

    def save_to_csv(df, filename):
        folder_path_map = {
            "Individual": "anonymised_csv_files/individual",
            "Programme": "anonymised_csv_files/programme",
            "Department": "anonymised_csv_files/department"
        }
        folder_path = Path(folder_path_map[data_category])
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
        file_path = folder_path / filename
        df.to_csv(file_path, index=False)
        return file_path

    def get_table_download_link(df, filename):
        """Generates a link allowing the csv file to be downloaded."""
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # B64 encode
        return f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download {filename}</a>'

    if uploaded_file is not None:
        pdf_date = extract_date_from_pdf(uploaded_file)
        
        with pdfplumber.open(uploaded_file) as pdf:
            first_page = pdf.pages[-1]
            second_page = pdf.pages[-2]
            third_page = pdf.pages[-3]
            table1 = first_page.extract_table()
            table2 = second_page.extract_table()
            table3 = third_page.extract_table()
            
            df_30_days = pd.DataFrame(table1)
            df_expertise_alignment_offtrack = pd.DataFrame(table2)
            df_appnps_lmroi_lmnps = pd.DataFrame(table3)

            # Process DF containing % learners without attendance for >30 days
            df_30_days = df_30_days.iloc[[2], [2]]  # Keep row index 2 and column index 2
            df_30_days.columns = ['Percentage of Learners Without Attendance in Last 30 Days']
            df_30_days.reset_index(drop=True, inplace=True)
            df_30_days["Date"] = pdf_date

            # Process DF containing coach expertise, alignment and % offtrack
            coach_expertise = df_expertise_alignment_offtrack.at[2, 4]
            coach_alignment = df_expertise_alignment_offtrack.at[2, 7]
            percentage_learners_offtrack = df_expertise_alignment_offtrack.at[2, 10]

            df_expertise_alignment_offtrack = pd.DataFrame({
                'Coach Expertise': [coach_expertise],
                'Coach Alignment': [coach_alignment],
                'Percentage of Learners Offtrack': [percentage_learners_offtrack]
            })
            df_expertise_alignment_offtrack["Date"] = pdf_date

            # Process DF containing NPS, AM ROI and AM NPS
            app_nps = df_appnps_lmroi_lmnps.at[2, 10]
            lm_roi = df_appnps_lmroi_lmnps.at[2, 7]
            lm_nps = df_appnps_lmroi_lmnps.at[2, 4]

            df_appnps_lmroi_lmnps = pd.DataFrame({
                'Apprentice NPS': [app_nps],
                'Manager ROI Score': [lm_roi],
                'Manager NPS': [lm_nps]
            })
            df_appnps_lmroi_lmnps["Date"] = pdf_date

            # Save the dataframes to CSV
            save_to_csv(df_30_days, f"df_30_days_{pdf_date}.csv")
            save_to_csv(df_expertise_alignment_offtrack, f"df_expertise_alignment_offtrack_{pdf_date}.csv")
            save_to_csv(df_appnps_lmroi_lmnps, f"df_appnps_lmroi_lmnps_{pdf_date}.csv")

            # Display the dataframes
            st.write("Percentage of Learners Without Attendance in Last 30 Days", df_30_days)
            st.write("Coach Expertise, Alignment and Percentage of Learners Offtrack", df_expertise_alignment_offtrack)
            st.write("Apprentice NPS, Manager ROI Score and Manager NPS", df_appnps_lmroi_lmnps)

            # Provide download links for the processed dataframes
            for df, name in zip([df_30_days, df_expertise_alignment_offtrack, df_appnps_lmroi_lmnps], 
                                [f"df_30_days_{pdf_date}.csv", f"df_expertise_alignment_offtrack_{pdf_date}.csv", f"df_appnps_lmroi_lmnps_{pdf_date}.csv"]):
                st.markdown(get_table_download_link(df, name), unsafe_allow_html=True)
