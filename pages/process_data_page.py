# import streamlit as st
# import pdfplumber
# from pathlib import Path
# import pandas as pd
# from helper_functions import extract_date_from_pdf, anonymise_apprentice_names
# import base64


# def process_data_page():

#     st.title("PDF Metrics Analysis")

#     # Add a radio button to select the data category
#     data_category = st.radio("Select Data Category:", ["Individual", "Programme", "Department"])

#     uploaded_file = st.file_uploader("Upload a PDF file", type=['pdf'])

#     def save_to_csv(df, filename):
#         # Determine the folder path based on data category
#         folder_path_map = {
#             "Individual": "anonymised_csv_files/individual",
#             "Programme": "anonymised_csv_files/programme",
#             "Department": "anonymised_csv_files/department"
#         }
#         folder_path = Path(folder_path_map[data_category])
#         if not folder_path.exists():
#             folder_path.mkdir(parents=True, exist_ok=True)
#         file_path = folder_path / filename
#         df.to_csv(file_path, index=False)
#         return file_path

#     def get_table_download_link(df, filename):
#         """Generates a link allowing the csv file to be downloaded."""
#         csv = df.to_csv(index=False)
#         b64 = base64.b64encode(csv.encode()).decode()  # B64 encode
#         return f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download {filename}</a>'

#     if uploaded_file is not None:
#         with pdfplumber.open(uploaded_file) as pdf:
#             # Extract PDF date and tables
#             pdf_date = extract_date_from_pdf(uploaded_file)
#             tables = [page.extract_table() for page in pdf.pages]

#             # Define dataframes and process them
#             df_lmnps = pd.DataFrame(tables[0])
#             df_lmroi = pd.DataFrame(tables[1])
#             df_offtrack = pd.DataFrame(tables[2])
#             df_last_attendance = pd.DataFrame(tables[3])
#             df_nps = pd.DataFrame(tables[7])
#             df_expertise_alignment = pd.DataFrame(tables[8])

#             # Remove rows 0, 1, 2 because they are empty
#             def drop_0_and_1(df):
#                 return df.drop([0,1])


#             df_lmnps = df_lmnps.drop([0,1])
#             df_lmroi = drop_0_and_1(df_lmroi)
#             df_offtrack = drop_0_and_1(df_offtrack)
#             df_last_attendance = drop_0_and_1(df_last_attendance)


#             # Remove columns 1 and 3 because they are empty
#             df_lmnps = df_lmnps.drop([1, 3], axis=1)
#             df_lmroi = df_lmroi.drop([1, 3], axis=1)
#             df_offtrack = df_offtrack.drop([1, 3], axis=1)
#             df_last_attendance = df_last_attendance.drop([1, 3, 4], axis=1)

#             # Remove nulls
#             df_lmnps = df_lmnps.dropna()
#             df_lmroi = df_lmroi.dropna()
#             df_offtrack = df_offtrack.dropna()
#             df_last_attendance = df_last_attendance.dropna()

#             # Reset Index
#             df_lmnps = df_lmnps.reset_index(drop=True)
#             df_lmroi = df_lmroi.reset_index(drop=True)
#             df_offtrack = df_offtrack.reset_index(drop=True)
#             df_last_attendance = df_last_attendance.reset_index(drop=True)

#             # Create new header including a date column
#             lmnps_header = ['Apprentice', 'LM NPS']
#             lmroi_header = ['Apprentice', 'LM ROI Out of 6']
#             offtrack_header = ['Apprentice', 'Status']
#             last_attendance_header = ['Apprentice', 'Days Since Last Attendance']

#             # Convert header to dataframe type
#             df_header_lmnps = pd.DataFrame([lmnps_header], columns=df_lmnps.columns)
#             df_header_lmroi = pd.DataFrame([lmroi_header], columns=df_lmroi.columns)
#             df_header_offtrack = pd.DataFrame([offtrack_header], columns=df_offtrack.columns)
#             df_header_last_attendance = pd.DataFrame([last_attendance_header], columns=df_last_attendance.columns)


#             # Concatenate header to df_lmnps datafram
#             df_lmnps = pd.concat([df_header_lmnps, df_lmnps]).reset_index(drop=True)
#             df_lmroi = pd.concat([df_header_lmroi, df_lmroi]).reset_index(drop=True)
#             df_offtrack = pd.concat([df_header_offtrack, df_offtrack]).reset_index(drop=True)
#             df_last_attendance = pd.concat([df_header_last_attendance, df_last_attendance]).reset_index(drop=True)


#             df_lmnps['Date'] = pdf_date
#             df_lmroi['Date'] = pdf_date
#             df_offtrack['Date'] = pdf_date
#             df_last_attendance['Date'] = pdf_date

#             # PROCESS FOR LM_NPS

#             df_lmnps = df_lmnps[df_lmnps[0] != '']

#             # Set the first row as the header
#             new_header = df_lmnps.iloc[0]
#             df_lmnps = df_lmnps[1:]
#             df_lmnps.columns = new_header

#             # Reset Index
#             df_lmnps = df_lmnps.reset_index(drop=True)
#             # print(df_lmnps)

#             new_header = ['Apprentice', 'LM NPS', 'Date']

#             # Set the new header for the first table (df_lmnps)
#             df_lmnps.columns = new_header
#             df_lmnps.index += 1

#             # Repeat the same steps for the other two tables: "df_lmroi" and "df_status"

#             # PROCESS FOR LM_ROI

#             df_lmroi = df_lmroi[df_lmroi[0] != '']

#             # Set the first row as the header
#             new_header_roi = df_lmroi.iloc[0]
#             df_lmroi = df_lmroi[1:]
#             df_lmroi.columns = new_header_roi

#             # Reset Index
#             df_lmroi = df_lmroi.reset_index(drop=True)

#             new_header_roi = ['Apprentice', 'LM ROI Out of 6', 'Date']

#             # Set the new header for the first table (df_lmnps)
#             df_lmroi.columns = new_header_roi
#             df_lmroi.index += 1

#             # PROCESS FOR OFF-TRACK/ON-TRACK

#             df_offtrack = df_offtrack[df_offtrack[0] != '']

#             # Set the first row as the header
#             new_header_offtrack = df_offtrack.iloc[0]
#             df_offtrack = df_offtrack[1:]
#             df_offtrack.columns = new_header_offtrack

#             # Reset Index
#             df_offtrack = df_offtrack.reset_index(drop=True)

#             new_header_offtrack = ['Apprentice', 'Status', 'Date']

#             # Set the new header for the first table (df_lmnps)
#             df_offtrack.columns = new_header_offtrack
#             df_offtrack.index += 1

#             # PROCESS FOR DAYS SINCE LAST ATTENDANCE

#             df_last_attendance = df_last_attendance[df_last_attendance[0] != '']

#             # Set the first row as the header
#             new_header_last_attendance = df_last_attendance.iloc[0]
#             df_last_attendance = df_last_attendance[1:]
#             df_last_attendance.columns = new_header_last_attendance

#             # Reset Index
#             df_last_attendance = df_last_attendance.reset_index(drop=True)

#             new_header_last_attendance = ['Apprentice', 'Days Since Last Attendance', 'Date']

#             # Set the new header for the first table (df_lmnps)
#             df_last_attendance.columns = new_header_last_attendance
#             df_last_attendance.index += 1

#             # PROCESS FOR NPS SCORE

#             # Extract nps score from table

#             # Extract the value from a specific cell
#             cell_value = df_nps.iat[2, 10]

#             # Create a DataFrame from the cell value
#             df_nps = pd.DataFrame([cell_value], columns=["Apprentice NPS"], index=[1])
#             df_nps['Date'] = pdf_date

#             # PROCESS FOR COACH EXPERTISE AND COACH ALIGNMENT

#             # Extract Expertise Value and Alignment Value

#             expertise_value = df_expertise_alignment.iat[2, 4]
#             alignment_value = df_expertise_alignment.iat[2, 7]

#             # Create DataFrame from cell values

#             df_expertise_alignment = pd.DataFrame({
#                 "Coach Expertise": expertise_value,
#                 "Coach Alignment": alignment_value
#             }, index=[1])

#             df_expertise_alignment["Date"] = pdf_date

#             # Anonymize apprentice names
#             df_lmnps = anonymise_apprentice_names(df_lmnps)
#             df_lmroi = anonymise_apprentice_names(df_lmroi)
#             df_offtrack = anonymise_apprentice_names(df_offtrack)
#             df_last_attendance = anonymise_apprentice_names(df_last_attendance)

#             # Save anonymized data to the specified folder
#             save_to_csv(df_lmnps, f"df_lmnps_{pdf_date}.csv")
#             save_to_csv(df_lmroi, f"df_lmroi_{pdf_date}.csv")
#             save_to_csv(df_offtrack, f"df_offtrack_{pdf_date}.csv")
#             save_to_csv(df_last_attendance, f"df_last_attendance_{pdf_date}.csv")
#             save_to_csv(df_expertise_alignment, f"df_expertise_alignment_{pdf_date}.csv")
#             save_to_csv(df_nps, f"df_nps_{pdf_date}.csv")

#             # Display dataframes

#             st.write("LM NPS Data", df_lmnps)
#             st.write("LM ROI Data", df_lmroi)
#             st.write("Offtrack Data", df_offtrack)
#             st.write("Last Attendance Data", df_last_attendance)

#             # Display NPS & Expertise/Alignment Data
            
#             st.write("Apprentice NPS", df_nps)
#             st.write("Coach Expertise & Alignment", df_expertise_alignment)

#             for df, name in zip([df_lmnps, df_lmroi, df_offtrack, df_last_attendance, df_nps, df_expertise_alignment], 
#                                 [f"df_lmnps_{pdf_date}.csv", f"df_lmroi_{pdf_date}.csv", 
#                                 f"df_offtrack_{pdf_date}.csv", f"df_last_attendance_{pdf_date}.csv",
#                                 f"df_last_attendance_{pdf_date}.csv", f"df_exerptise_alignment_{pdf_date}.csv",]):
#                 st.markdown(get_table_download_link(df, name), unsafe_allow_html=True)

import streamlit as st
import pdfplumber
from pathlib import Path
import pandas as pd
from helper_functions import extract_date_from_pdf, anonymise_apprentice_names
import base64

def process_data_page():
    st.title("PDF Metrics Analysis")

    # Add a radio button to select the data category (Individual, Team, Department)
    data_category = st.radio("Select Data Category:", ["Individual", "Team", "Department"])

    uploaded_file = st.file_uploader("Upload a PDF file", type=['pdf'])

    def save_to_csv(df, filename):
        folder_path_map = {
            "Individual": "anonymised_csv_files/individual",
            "Team": "anonymised_csv_files/team",
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
