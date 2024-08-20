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

    # Combine all data
    combined_data = pd.concat([individual_data, department_data, programme_data], ignore_index=True)

    # Check if there is any data available
    if combined_data.empty:
        st.title('Comparison of Metrics Over Time')
        st.write('No data to display')
        return

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
    st.title('Comparison of Metrics Over Time')

    # Function to create plots for a given metric with optional y-axis range
    def create_plot(y_column, title, yaxis_title, yaxis_range=None):
        if y_column in grouped_data.columns and not grouped_data[y_column].dropna().empty:
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
        else:
            st.write(f'No data to display for {title}')

    # Create visualizations
    st.header('Coach Expertise')
    create_plot('Coach Expertise', 'Coach Expertise', 'Coach Expertise Score', yaxis_range=[1, 6])

    st.header('Coach Alignment')
    create_plot('Coach Alignment', 'Coach Alignment', 'Coach Alignment Score', yaxis_range=[1, 6])

    st.header('Apprentice NPS')
    create_plot('Apprentice NPS', 'Apprentice NPS', 'Apprentice NPS')

    st.header('Manager ROI Score')
    create_plot('Manager ROI Score', 'Manager ROI Score', 'Manager ROI Score', yaxis_range=[1, 6])

    st.header('Manager NPS')
    create_plot('Manager NPS', 'Manager NPS', 'Manager NPS')

    st.header('Percentage of Learners Without Attendance')
    create_plot('Percentage of Learners Without Attendance in Last 30 Days', 'Learners Without Attendance in Last 30 Days', 'Percentage')

    st.header('Percentage of Learners Off Track')
    create_plot('Percentage of Learners Offtrack', 'Percentage of Learners Off Track', 'Percentage')