import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def visualise_data_page():

    # Reading the CSV files
    days_30_data = pd.read_csv('anonymised_csv_files/individual/df_30_days_2024-08-17.csv')
    appnps_data = pd.read_csv('anonymised_csv_files/individual/df_appnps_lmroi_lmnps_2024-08-17.csv')
    expertise_data = pd.read_csv('anonymised_csv_files/individual/df_expertise_alignment_offtrack_2024-08-17.csv')

    # Make sure 'Date' columns are in datetime format
    days_30_data['Date'] = pd.to_datetime(days_30_data['Date'])
    appnps_data['Date'] = pd.to_datetime(appnps_data['Date'])
    expertise_data['Date'] = pd.to_datetime(expertise_data['Date'])

    # Setting the title
    st.title('Educational Data Dashboard')

    # Coach Expertise Visualization
    st.header('Coach Expertise Over Time')
    fig = px.line(expertise_data, x='Date', y='Coach Expertise', markers=True, title='Coach Expertise Over Time')
    fig.update_layout(
        yaxis_title='Coach Expertise Score',
        xaxis=dict(tickformat='%d-%m-%Y')
    )
    st.plotly_chart(fig)

    # Coach Alignment Visualization
    st.header('Coach Alignment Over Time')
    fig = px.line(expertise_data, x='Date', y='Coach Alignment', markers=True, title='Coach Alignment Over Time')
    fig.update_layout(
        yaxis_title='Coach Alignment Score',
        xaxis=dict(tickformat='%d-%m-%Y')
    )
    st.plotly_chart(fig)

    # Apprentice NPS Visualization
    st.header('Apprentice NPS Over Time')
    fig = px.line(appnps_data, x='Date', y='Apprentice NPS', markers=True, title='Apprentice NPS Over Time')
    fig.update_layout(
        yaxis_title='Apprentice NPS Score',
        xaxis=dict(tickformat='%d-%m-%Y')
    )
    st.plotly_chart(fig)

    # Manager ROI Score Visualization
    st.header('Manager ROI Score Over Time')
    fig = px.line(appnps_data, x='Date', y='Manager ROI Score', markers=True, title='Manager ROI Score Over Time')
    fig.update_traces(line_color='red')
    fig.update_layout(
        yaxis_title='Manager ROI Score',
        xaxis=dict(tickformat='%d-%m-%Y')
    )
    st.plotly_chart(fig)

    # Manager NPS Visualization
    st.header('Manager NPS Over Time')
    fig = px.line(appnps_data, x='Date', y='Manager NPS', markers=True, title='Manager NPS Over Time')
    fig.update_traces(line_color='green')
    fig.update_layout(
        yaxis_title='Manager NPS Score',
        xaxis=dict(tickformat='%d-%m-%Y')
    )
    st.plotly_chart(fig)

    # Attendance Data Visualization
    st.header('Percentage of Learners Without Attendance Over Time')
    days_30_data['Percentage of Learners Without Attendance in Last 30 Days'] = days_30_data['Percentage of Learners Without Attendance in Last 30 Days'].str.rstrip('%').astype(float)
    fig = px.line(days_30_data, x='Date', y='Percentage of Learners Without Attendance in Last 30 Days', markers=True, title='Learners Without Attendance in Last 30 Days Over Time')
    fig.update_layout(
        yaxis_title='Percentage',
        xaxis=dict(tickformat='%d-%m-%Y')
    )
    st.plotly_chart(fig)

    # Percentage of Learners Off Track Visualization
    st.header('Percentage of Learners Off Track Over Time')
    expertise_data['Percentage of Learners Offtrack'] = expertise_data['Percentage of Learners Offtrack'].str.rstrip('%').astype(float)
    fig = px.line(expertise_data, x='Date', y='Percentage of Learners Offtrack', markers=True, title='Percentage of Learners Off Track Over Time')
    fig.update_traces(line_color='purple')
    fig.update_layout(
        yaxis_title='Percentage',
        xaxis=dict(tickformat='%d-%m-%Y')
    )
    st.plotly_chart(fig)