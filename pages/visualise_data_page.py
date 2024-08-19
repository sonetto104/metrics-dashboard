import streamlit as st
import pandas as pd
import plotly.express as px
import glob
import os


def visualise_data_page():

    # Function to read and process all CSV files in a given directory
    def read_all_csv_files_in_directory(directory):
        dfs = {}
        for file in glob.glob(directory + '/*.csv'):
            prefix = os.path.basename(file).split('_')[0]
            if prefix in dfs:
                dfs[prefix] = pd.concat([dfs[prefix], pd.read_csv(file)])
            else:
                dfs[prefix] = pd.read_csv(file)
        return dfs

    # Load the initial dataframes for individual, programme, and department data
    dfs_individual = read_all_csv_files_in_directory('anonymised_csv_files/individual')
    dfs_programme = read_all_csv_files_in_directory('anonymised_csv_files/programme')
    dfs_department = read_all_csv_files_in_directory('anonymised_csv_files/department')

    # Function to create line graph for each metric
    def line_graph(dfs, metric, title):
        fig = px.line()
        for key, df in dfs.items():
            if metric in df.columns:
                fig.add_scatter(x=df['Date'], y=df[metric], mode='lines', name=key)
        fig.update_layout(title=title)
        st.plotly_chart(fig)

    # Display the line graphs in the streamlit app
    st.title('Metrics Visualisation for Individual, Programme, and Department')

    # Loop through each metric and create line graphs for comparison
    for metric in set().union(*[df.columns for df in dfs_individual.values()] +
                            [df.columns for df in dfs_programme.values()] +
                            [df.columns for df in dfs_department.values()]):
        if metric != 'Date':
            title = f'{metric} over time for Individual, Programme, and Department'
            line_graph(dfs_individual, metric, title)