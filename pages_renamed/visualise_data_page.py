# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go

# def visualise_data_page():

#     # Reading the CSV files
#     days_30_data = pd.read_csv('anonymised_csv_files/individual/df_30_days_2024-08-17.csv')
#     appnps_data = pd.read_csv('anonymised_csv_files/individual/df_appnps_lmroi_lmnps_2024-08-17.csv')
#     expertise_data = pd.read_csv('anonymised_csv_files/individual/df_expertise_alignment_offtrack_2024-08-17.csv')

#     # Make sure 'Date' columns are in datetime format
#     days_30_data['Date'] = pd.to_datetime(days_30_data['Date'])
#     appnps_data['Date'] = pd.to_datetime(appnps_data['Date'])
#     expertise_data['Date'] = pd.to_datetime(expertise_data['Date'])

#     # Setting the title
#     st.title('Educational Data Dashboard')

#     # Coach Expertise Visualization
#     st.header('Coach Expertise Over Time')
#     fig = px.line(expertise_data, x='Date', y='Coach Expertise', markers=True, title='Coach Expertise Over Time')
#     fig.update_layout(
#         yaxis_title='Coach Expertise Score',
#         xaxis=dict(tickformat='%d-%m-%Y')
#     )
#     st.plotly_chart(fig)

#     # Coach Alignment Visualization
#     st.header('Coach Alignment Over Time')
#     fig = px.line(expertise_data, x='Date', y='Coach Alignment', markers=True, title='Coach Alignment Over Time')
#     fig.update_layout(
#         yaxis_title='Coach Alignment Score',
#         xaxis=dict(tickformat='%d-%m-%Y')
#     )
#     st.plotly_chart(fig)

#     # Apprentice NPS Visualization
#     st.header('Apprentice NPS Over Time')
#     fig = px.line(appnps_data, x='Date', y='Apprentice NPS', markers=True, title='Apprentice NPS Over Time')
#     fig.update_layout(
#         yaxis_title='Apprentice NPS Score',
#         xaxis=dict(tickformat='%d-%m-%Y')
#     )
#     st.plotly_chart(fig)

#     # Manager ROI Score Visualization
#     st.header('Manager ROI Score Over Time')
#     fig = px.line(appnps_data, x='Date', y='Manager ROI Score', markers=True, title='Manager ROI Score Over Time')
#     fig.update_traces(line_color='red')
#     fig.update_layout(
#         yaxis_title='Manager ROI Score',
#         xaxis=dict(tickformat='%d-%m-%Y')
#     )
#     st.plotly_chart(fig)

#     # Manager NPS Visualization
#     st.header('Manager NPS Over Time')
#     fig = px.line(appnps_data, x='Date', y='Manager NPS', markers=True, title='Manager NPS Over Time')
#     fig.update_traces(line_color='green')
#     fig.update_layout(
#         yaxis_title='Manager NPS Score',
#         xaxis=dict(tickformat='%d-%m-%Y')
#     )
#     st.plotly_chart(fig)

#     # Attendance Data Visualization
#     st.header('Percentage of Learners Without Attendance Over Time')
#     days_30_data['Percentage of Learners Without Attendance in Last 30 Days'] = days_30_data['Percentage of Learners Without Attendance in Last 30 Days'].str.rstrip('%').astype(float)
#     fig = px.line(days_30_data, x='Date', y='Percentage of Learners Without Attendance in Last 30 Days', markers=True, title='Learners Without Attendance in Last 30 Days Over Time')
#     fig.update_layout(
#         yaxis_title='Percentage',
#         xaxis=dict(tickformat='%d-%m-%Y')
#     )
#     st.plotly_chart(fig)

#     # Percentage of Learners Off Track Visualization
#     st.header('Percentage of Learners Off Track Over Time')
#     expertise_data['Percentage of Learners Offtrack'] = expertise_data['Percentage of Learners Offtrack'].str.rstrip('%').astype(float)
#     fig = px.line(expertise_data, x='Date', y='Percentage of Learners Offtrack', markers=True, title='Percentage of Learners Off Track Over Time')
#     fig.update_traces(line_color='purple')
#     fig.update_layout(
#         yaxis_title='Percentage',
#         xaxis=dict(tickformat='%d-%m-%Y')
#     )
#     st.plotly_chart(fig)

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import os
# from glob import glob

# def load_data(directory_pattern):
#     all_files = glob(directory_pattern)
#     dfs = [pd.read_csv(f) for f in all_files]
#     if dfs:
#         combined_df = pd.concat(dfs, ignore_index=True)
#     else:
#         combined_df = pd.DataFrame()  # Return an empty DataFrame if no files are found
#     return combined_df

# def visualise_data_page():
#     # Load data from all required directories
#     individual_pattern = 'anonymised_csv_files/individual/*.csv'
#     department_pattern = 'anonymised_csv_files/department/*.csv'
#     programme_pattern = 'anonymised_csv_files/programme/*.csv'

#     # Load data while maintaining separation between individual, department, and programme
#     individual_data = load_data(individual_pattern)
#     department_data = load_data(department_pattern)
#     programme_data = load_data(programme_pattern)

#     # Ensure 'Date' columns are in datetime format for each DataFrame
#     for df in [individual_data, department_data, programme_data]:
#         if not df.empty:
#             df['Date'] = pd.to_datetime(df['Date'])

#     # Add Source column to each DataFrame to differentiate them in plots
#     if not individual_data.empty:
#         individual_data['Source'] = 'Individual'
#     if not department_data.empty:
#         department_data['Source'] = 'Department'
#     if not programme_data.empty:
#         programme_data['Source'] = 'Programme'

#     # Setting the title
#     st.title('Educational Data Dashboard')

#     # Function to create plots for a given metric
#     def create_plot(dataframe, y_column, title, yaxis_title):
#         combined_data = pd.concat([df for df in [individual_data, department_data, programme_data] if not df.empty])
#         fig = px.line(combined_data, x='Date', y=y_column, color='Source', markers=True, title=title)
#         fig.update_layout(
#             yaxis_title=yaxis_title,
#             xaxis=dict(tickformat='%d-%m-%Y')
#         )
#         st.plotly_chart(fig)

#     # Coach Expertise Visualization
#     st.header('Coach Expertise Over Time')
#     create_plot(individual_data, 'Coach Expertise', 'Coach Expertise Over Time', 'Coach Expertise Score')
#     create_plot(programme_data, 'Coach Expertise', 'Coach Expertise Over Time', 'Coach Expertise Score')
#     # Coach Alignment Visualization
#     st.header('Coach Alignment Over Time')
#     create_plot(individual_data, 'Coach Alignment', 'Coach Alignment Over Time', 'Coach Alignment Score')
#     create_plot(programme_data, 'Coach Alignment', 'Coach Alignment Over Time', 'Coach Alignment Score')

#     # Apprentice NPS Visualization
#     st.header('Apprentice NPS Over Time')
#     create_plot(individual_data, 'Apprentice NPS', 'Apprentice NPS Over Time', 'Apprentice NPS Score')
#     create_plot(programme_data, 'Apprentice NPS', 'Apprentice NPS Over Time', 'Apprentice NPS Score')
#     # Manager ROI Score Visualization
#     st.header('Manager ROI Score Over Time')
#     create_plot(individual_data, 'Manager ROI Score', 'Manager ROI Score Over Time', 'Manager ROI Score')
#     create_plot(programme_data, 'Manager ROI Score', 'Manager ROI Score Over Time', 'Manager ROI Score')
#     # Manager NPS Visualization
#     st.header('Manager NPS Over Time')
#     create_plot(individual_data, 'Manager NPS', 'Manager NPS Over Time', 'Manager NPS Score')
#     create_plot(programme_data, 'Manager NPS', 'Manager NPS Over Time', 'Manager NPS Score')

    # Attendance Data Visualization
    # st.header('Percentage of Learners Without Attendance Over Time')
    # combined_attendance = pd.concat([df for df in [individual_data, department_data, programme_data] if not df.empty])
    # if not combined_attendance.empty:
    #     combined_attendance['Percentage of Learners Without Attendance in Last 30 Days'] = combined_attendance['Percentage of Learners Without Attendance in Last 30 Days'].str.rstrip('%').astype(float)
    # create_plot(combined_attendance, 'Percentage of Learners Without Attendance in Last 30 Days', 'Learners Without Attendance in Last 30 Days Over Time', 'Percentage')

    # Percentage of Learners Off Track Visualization
    # st.header('Percentage of Learners Off Track Over Time')
    # combined_offtrack = pd.concat([df for df in [individual_data, department_data, programme_data] if not df.empty])
    # if not combined_offtrack.empty:
    #     combined_offtrack['Percentage of Learners Offtrack'] = combined_offtrack['Percentage of Learners Offtrack'].str.rstrip('%').astype(float)
    # create_plot(combined_offtrack, 'Percentage of Learners Offtrack', 'Percentage of Learners Off Track Over Time', 'Percentage')

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import os
# from glob import glob

# def load_data(directory_pattern, source):
#     all_files = glob(directory_pattern)
#     dfs = [pd.read_csv(f) for f in all_files]
#     if dfs:
#         combined_df = pd.concat(dfs, ignore_index=True)
#         combined_df['Source'] = source  # Add a source column to identify the data source
#     else:
#         combined_df = pd.DataFrame()  # Return an empty DataFrame if no files are found
#     return combined_df

# def visualise_data_page():
#     # Load data from all required directories
#     individual_data = load_data('anonymised_csv_files/individual/*.csv', 'Individual')
#     department_data = load_data('anonymised_csv_files/department/*.csv', 'Department')
#     programme_data = load_data('anonymised_csv_files/programme/*.csv', 'Programme')

#     # Ensure 'Date' columns are in datetime format for each DataFrame
#     for df in [individual_data, department_data, programme_data]:
#         if not df.empty:
#             df['Date'] = pd.to_datetime(df['Date'])

#     # Combine all data for each metric
#     combined_data = pd.concat([df for df in [individual_data, department_data, programme_data] if not df.empty])

#     # Setting the title
#     st.title('Educational Data Dashboard')

#     # Function to create plots for a given metric
#     def create_plot(y_column, title, yaxis_title):
#         fig = px.line(combined_data, x='Date', y=y_column, color='Source', markers=True, title=title)
#         fig.update_layout(
#             yaxis_title=yaxis_title,
#             xaxis=dict(tickformat='%d-%m-%Y')
#         )
#         st.plotly_chart(fig)

#     # Coach Expertise Visualization
#     st.header('Coach Expertise Over Time')
#     create_plot('Coach Expertise', 'Coach Expertise Over Time', 'Coach Expertise Score')

#     # Coach Alignment Visualization
#     st.header('Coach Alignment Over Time')
#     create_plot('Coach Alignment', 'Coach Alignment Over Time', 'Coach Alignment Score')

#     # Apprentice NPS Visualization
#     st.header('Apprentice NPS Over Time')
#     create_plot('Apprentice NPS', 'Apprentice NPS Over Time', 'Apprentice NPS Score')

#     # Manager ROI Score Visualization
#     st.header('Manager ROI Score Over Time')
#     create_plot('Manager ROI Score', 'Manager ROI Score Over Time', 'Manager ROI Score')

#     # Manager NPS Visualization
#     st.header('Manager NPS Over Time')
#     create_plot('Manager NPS', 'Manager NPS Over Time', 'Manager NPS Score')

#     # Attendance Data Visualization
#     st.header('Percentage of Learners Without Attendance Over Time')
#     combined_data['Percentage of Learners Without Attendance in Last 30 Days'] = combined_data['Percentage of Learners Without Attendance in Last 30 Days'].str.rstrip('%').astype(float)
#     create_plot('Percentage of Learners Without Attendance in Last 30 Days', 'Learners Without Attendance in Last 30 Days Over Time', 'Percentage')

#     # Percentage of Learners Off Track Visualization
#     st.header('Percentage of Learners Off Track Over Time')
#     combined_data['Percentage of Learners Offtrack'] = combined_data['Percentage of Learners Offtrack'].str.rstrip('%').astype(float)
#     create_plot('Percentage of Learners Offtrack', 'Percentage of Learners Off Track Over Time', 'Percentage')

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from glob import glob

# def load_data(directory_pattern, source):
#     all_files = glob(directory_pattern)
#     dfs = [pd.read_csv(f) for f in all_files]
#     if dfs:
#         combined_df = pd.concat(dfs, ignore_index=True)
#         combined_df['Source'] = source  # Add a source column to identify the data source
#     else:
#         combined_df = pd.DataFrame()  # Return an empty DataFrame if no files are found
#     return combined_df

# def visualise_data_page():
#     # Load data from all required directories
#     individual_data = load_data('anonymised_csv_files/individual/*.csv', 'Individual')
#     department_data = load_data('anonymised_csv_files/department/*.csv', 'Department')
#     programme_data = load_data('anonymised_csv_files/programme/*.csv', 'Programme')

#     # Combine all data for each metric
#     combined_data = pd.concat([individual_data, department_data, programme_data], ignore_index=True)

#     # Ensure 'Date' column is in datetime format
#     combined_data['Date'] = pd.to_datetime(combined_data['Date'])

#     # Convert percentage columns to floats properly, if they exist
#     if 'Percentage of Learners Without Attendance in Last 30 Days' in combined_data.columns:
#         combined_data['Percentage of Learners Without Attendance in Last 30 Days'] = (
#             combined_data['Percentage of Learners Without Attendance in Last 30 Days']
#             .str.rstrip('%')
#             .astype(float)
#         )

#     if 'Percentage of Learners Offtrack' in combined_data.columns:
#         combined_data['Percentage of Learners Offtrack'] = (
#             combined_data['Percentage of Learners Offtrack']
#             .str.rstrip('%')
#             .astype(float)
#         )

#     # Identify and remove any duplicate entries
#     combined_data.drop_duplicates(inplace=True)

#     # Check for any potential missing values that could cause breaks
#     combined_data.fillna(method='ffill', inplace=True)

#     # Setting the title
#     st.title('Educational Data Dashboard')

#     # Function to create plots for a given metric
#     def create_plot(y_column, title, yaxis_title):
#         fig = px.line(
#             combined_data, 
#             x='Date', 
#             y=y_column, 
#             color='Source', 
#             markers=True, 
#             title=title
#         )
#         fig.update_layout(
#             yaxis_title=yaxis_title,
#             xaxis=dict(tickformat='%d-%m-%Y')
#         )
#         st.plotly_chart(fig)

#     # Coach Expertise Visualization
#     st.header('Coach Expertise Over Time')
#     create_plot('Coach Expertise', 'Coach Expertise Over Time', 'Coach Expertise Score')

#     # Coach Alignment Visualization
#     st.header('Coach Alignment Over Time')
#     create_plot('Coach Alignment', 'Coach Alignment Over Time', 'Coach Alignment Score')

#     # Apprentice NPS Visualization
#     st.header('Apprentice NPS Over Time')
#     create_plot('Apprentice NPS', 'Apprentice NPS Over Time', 'Apprentice NPS Score')

#     # Manager ROI Score Visualization
#     st.header('Manager ROI Score Over Time')
#     create_plot('Manager ROI Score', 'Manager ROI Score Over Time', 'Manager ROI Score')

#     # Manager NPS Visualization
#     st.header('Manager NPS Over Time')
#     create_plot('Manager NPS', 'Manager NPS Over Time', 'Manager NPS Score')

#     # Attendance Data Visualization
#     st.header('Percentage of Learners Without Attendance Over Time')
#     create_plot('Percentage of Learners Without Attendance in Last 30 Days', 'Learners Without Attendance in Last 30 Days Over Time', 'Percentage')

#     # Percentage of Learners Off Track Visualization
#     st.header('Percentage of Learners Off Track Over Time')
#     create_plot('Percentage of Learners Offtrack', 'Percentage of Learners Off Track Over Time', 'Percentage')

import streamlit as st
import pandas as pd
import plotly.express as px
from glob import glob

def load_data(directory_pattern, source):
    all_files = glob(directory_pattern)
    dfs = [pd.read_csv(f) for f in all_files]
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df['Source'] = source  # Add a source column to identify the data source
    else:
        combined_df = pd.DataFrame()  # Return an empty DataFrame if no files are found
    return combined_df

def visualise_data_page():
    # Load data from all required directories
    individual_data = load_data('anonymised_csv_files/individual/*.csv', 'Individual')
    department_data = load_data('anonymised_csv_files/department/*.csv', 'Department')
    programme_data = load_data('anonymised_csv_files/programme/*.csv', 'Programme')

    # Combine all data for each metric
    combined_data = pd.concat([individual_data, department_data, programme_data], ignore_index=True)

    # Ensure 'Date' column is in datetime format
    combined_data['Date'] = pd.to_datetime(combined_data['Date'])

    # Remove any exact duplicate rows
    combined_data.drop_duplicates(inplace=True)

    # Convert percentage columns to floats properly, if they exist
    if 'Percentage of Learners Without Attendance in Last 30 Days' in combined_data.columns:
        combined_data['Percentage of Learners Without Attendance in Last 30 Days'] = (
            combined_data['Percentage of Learners Without Attendance in Last 30 Days']
            .str.rstrip('%')
            .astype(float)
        )

    if 'Percentage of Learners Offtrack' in combined_data.columns:
        combined_data['Percentage of Learners Offtrack'] = (
            combined_data['Percentage of Learners Offtrack']
            .str.rstrip('%')
            .astype(float)
        )
    
    # Ensure that there's only one entry per Date and Source combination
    grouped_data = combined_data.groupby(['Date', 'Source']).first().reset_index()

    # Setting the title
    st.title('Educational Data Dashboard')

    # Function to create plots for a given metric with optional y-axis range
    def create_plot(y_column, title, yaxis_title, yaxis_range=None):
        fig = px.line(
            grouped_data, 
            x='Date', 
            y=y_column, 
            color='Source', 
            markers=True, 
            title=title
        )
        fig.update_layout(
            yaxis_title=yaxis_title,
            xaxis=dict(tickformat='%d-%m-%Y')
        )
        if yaxis_range:
            fig.update_yaxes(range=yaxis_range)
        st.plotly_chart(fig)

    # Coach Expertise Visualization
    st.header('Coach Expertise Over Time')
    create_plot('Coach Expertise', 'Coach Expertise Over Time', 'Coach Expertise Score', yaxis_range=[1, 6])

    # Coach Alignment Visualization
    st.header('Coach Alignment Over Time')
    create_plot('Coach Alignment', 'Coach Alignment Over Time', 'Coach Alignment Score', yaxis_range=[1, 6])

    # Apprentice NPS Visualization
    st.header('Apprentice NPS Over Time')
    create_plot('Apprentice NPS', 'Apprentice NPS Over Time', 'Apprentice NPS Score')

    # Manager ROI Score Visualization
    st.header('Manager ROI Score Over Time')
    create_plot('Manager ROI Score', 'Manager ROI Score Over Time', 'Manager ROI Score', yaxis_range=[1, 6])

    # Manager NPS Visualization
    st.header('Manager NPS Over Time')
    create_plot('Manager NPS', 'Manager NPS Over Time', 'Manager NPS Score')

    # Attendance Data Visualization
    st.header('Percentage of Learners Without Attendance Over Time')
    create_plot('Percentage of Learners Without Attendance in Last 30 Days', 'Learners Without Attendance in Last 30 Days Over Time', 'Percentage')

    # Percentage of Learners Off Track Visualization
    st.header('Percentage of Learners Off Track Over Time')
    create_plot('Percentage of Learners Offtrack', 'Percentage of Learners Off Track Over Time', 'Percentage')