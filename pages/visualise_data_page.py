import streamlit as st
import pandas as pd
from pathlib import Path
import glob
import plotly.express as px 
import plotly.graph_objects as go

def load_and_concat_data(pattern):
    files = glob.glob(pattern)
    if files:
        return pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
    else:
        return pd.DataFrame()

def visualize_data_page():
    st.title("Historical Metrics Visualization")

    base_path = "anonymised_csv_files"
    categories = ["individual", "programme", "department"]
    
    data = {
        category: {
            "lmnps": load_and_concat_data(f"{base_path}/{category}/df_lmnps_*.csv"),
            "lmroi": load_and_concat_data(f"{base_path}/{category}/df_lmroi_*.csv"),
            "offtrack": load_and_concat_data(f"{base_path}/{category}/df_offtrack_*.csv"),
            "last_attendance": load_and_concat_data(f"{base_path}/{category}/df_last_attendance_*.csv"),
            "expertise_alignment": load_and_concat_data(f"{base_path}/{category}/df_expertise_alignment_*.csv"),
            "nps": load_and_concat_data(f"{base_path}/{category}/df_nps_*.csv")
        }
        for category in categories
    }

    # Function to plot the graphs for each metric and category
    def plot_metric(metric, y_label, title):
        fig = go.Figure()
        for category, dfs in data.items():
            df = dfs[metric]
            if not df.empty:
                grouped_data = df.groupby('Date')[y_label].mean().reset_index()
                fig.add_trace(
                    go.Scatter(
                        x=grouped_data['Date'], 
                        y=grouped_data[y_label], 
                        mode='lines', 
                        name=f'{category.capitalize()} {y_label}'
                    )
                )
        fig.update_layout(
            title=title,
            xaxis_title='Date',
            yaxis_title=y_label,
            legend_title='Category'
        )
        st.plotly_chart(fig)
    
    # LM NPS
    plot_metric("lmnps", "LM NPS", "Average LM NPS Over Time")

    # LM ROI
    plot_metric("lmroi", "LM ROI Out of 6", "Average LM ROI Over Time")

    # Off-track status
    fig_offtrack = go.Figure()
    for category, dfs in data.items():
        df = dfs["offtrack"]
        if not df.empty:
            status_count_over_time = df.groupby(['Date', 'Status']).size().unstack(fill_value=0).reset_index()
            if 'On-Track' in status_count_over_time.columns:
                fig_offtrack.add_trace(
                    go.Scatter(
                        x=status_count_over_time['Date'], 
                        y=status_count_over_time['On-Track'], 
                        mode='lines', 
                        name=f'{category.capitalize()} On-Track'
                    )
                )
            if 'Off-Track' in status_count_over_time.columns:
                fig_offtrack.add_trace(
                    go.Scatter(
                        x=status_count_over_time['Date'], 
                        y=status_count_over_time['Off-Track'], 
                        mode='lines', 
                        name=f'{category.capitalize()} Off-Track'
                    )
                )
    fig_offtrack.update_layout(
        title='On Track vs Off Track Over Time',
        xaxis_title='Date',
        yaxis_title='Count',
        legend_title='Status'
    )
    st.plotly_chart(fig_offtrack)

    # Last Attendance
    plot_metric("last_attendance", "Days Since Last Attendance", "Average Days Since Last Attendance Over Time")

    # Coach Expertise and Alignment
    plot_metric("expertise_alignment", "Coach Expertise", "Average Coach Expertise Over Time")
    plot_metric("expertise_alignment", "Coach Alignment", "Average Coach Alignment Over Time")

    # Apprentice NPS Score
    plot_metric("nps", "Apprentice NPS", "Average Apprentice NPS Over Time")

if __name__ == "__main__":
    visualize_data_page()










# import streamlit as st
# import pandas as pd
# from pathlib import Path
# import glob
# import plotly.express as px 
# import plotly.graph_objects as go  # Import Plotly graph_objects

# def visualize_data_page():
#     st.title("Historical Metrics Visualization")

#     base_path = "anonymised_csv_files"
#     categories = ["individual", "team", "department"]
    
#     data = {
#         category: {
#             "lmnps": load_and_concat_data(f"{base_path}/{category}/df_lmnps_*.csv"),
#             "lmroi": load_and_concat_data(f"{base_path}/{category}/df_lmroi_*.csv"),
#             "offtrack": load_and_concat_data(f"{base_path}/{category}/df_offtrack_*.csv"),
#             "last_attendance": load_and_concat_data(f"{base_path}/{category}/df_last_attendance_*.csv"),
#             "expertise_alignment": load_and_concat_data(f"{base_path}/{category}/df_expertise_alignment_*.csv"),
#             "nps": load_and_concat_data(f"{base_path}/{category}/df_nps_*.csv")
#         }
#         for category in categories
#     }

#     st.write("Data Categories", data)

#     for metric in ["lmnps", "lmroi", "offtrack", "last_attendance", "expertise_alignment", "nps"]:
#         for category in categories:
#             df = data[category][metric]
#             if metric == "offtrack":
#                 status_count_over_time = df.groupby(['Date', 'Status']).size().unstack(fill_value=0).reset_index()
#                 fig = go.Figure()
#                 if 'On-Track' in status_count_over_time.columns:
#                     fig.add_trace(
#                         go.Scatter(
#                             x=status_count_over_time['Date'], 
#                             y=status_count_over_time['On-Track'], 
#                             mode='lines', 
#                             name=f'{category.capitalize()} On-Track'
#                         )
#                     )
#                 if 'Off-Track' in status_count_over_time.columns:
#                     fig.add_trace(
#                         go.Scatter(
#                             x=status_count_over_time['Date'], 
#                             y=status_count_over_time['Off-Track'], 
#                             mode='lines', 
#                             name=f'{category.capitalize()} Off-Track'
#                         )
#                     )
#             else:
#                 groupby_column = 'Date'
#                 metric_column = df.columns[1]  # Assumes second column is the metric column
#                 mean_metric_over_time = df.groupby(groupby_column)[metric_column].mean().reset_index()
#                 fig = px.line(mean_metric_over_time, x=groupby_column, y=metric_column, title=f'Average {metric.capitalize()} Over Time')
            
#             st.plotly_chart(fig)


    
    # # Load all CSV files from the data directory
    # data_path = Path("anonymised_csv_files")
    
    # if data_path.exists():
    #     lmnps_files = glob.glob(str(data_path / "df_lmnps_*.csv"))
    #     lmroi_files = glob.glob(str(data_path / "df_lmroi_*.csv"))
    #     offtrack_files = glob.glob(str(data_path / "df_offtrack_*.csv"))
    #     last_attendance_files = glob.glob(str(data_path / "df_last_attendance_*.csv"))
    #     expertise_alignment_files = glob.glob(str(data_path / "df_expertise_alignment_*.csv"))
    #     nps_files = glob.glob(str(data_path / "df_nps_*.csv"))
        
    #     df_lmnps = pd.concat((pd.read_csv(f) for f in lmnps_files), ignore_index=True)
    #     df_lmroi = pd.concat((pd.read_csv(f) for f in lmroi_files), ignore_index=True)
    #     df_offtrack = pd.concat((pd.read_csv(f) for f in offtrack_files), ignore_index=True)
    #     df_last_attendance = pd.concat((pd.read_csv(f) for f in last_attendance_files), ignore_index=True)
    #     df_expertise_alignment = pd.concat((pd.read_csv(f) for f in expertise_alignment_files), ignore_index=True)
    #     df_nps = pd.concat((pd.read_csv(f) for f in nps_files), ignore_index=True)
    #     st.write("LM NPS Historical Data", df_lmnps)
    #     st.write("LM ROI Historical Data", df_lmroi)
    #     st.write("Offtrack Historical Data", df_offtrack)
    #     st.write("Last Attendance Historical Data", df_last_attendance)
    #     st.write("Coach Expertise and Alignment Historical Data", df_expertise_alignment)
    #     st.write("NPS Score Historical Data", df_nps)
        
    #     # Visualizations
        
    #     mean_lmnps_over_time = df_lmnps.groupby('Date')['LM NPS'].mean().reset_index()

    #     # Create Plotly line chart
    #     fig = px.line(mean_lmnps_over_time, x='Date', y='LM NPS', title='Average NPS Score Over Time')
        
    #     # Display the Plotly chart in Streamlit
    #     st.plotly_chart(fig)

    #     mean_lmroi_over_time = df_lmroi.groupby('Date')['LM ROI Out of 6'].mean().reset_index()
    #     fig_lmroi = px.line(mean_lmroi_over_time, x='Date', y='LM ROI Out of 6', title='Average LM ROI Score Over Time')
    #     st.plotly_chart(fig_lmroi)

    #     # Offtrack Status: Calculate the count of "On Track" and "Offtrack" status for each date
    #     status_count_over_time = df_offtrack.groupby(['Date', 'Status']).size().unstack(fill_value=0).reset_index()
        
    #     # Inspect the DataFrame's contents
    #     st.write(status_count_over_time)

    #     # Create the line graph
    #     fig_offtrack = go.Figure()
    #     if 'On-Track' in status_count_over_time.columns:
    #         fig_offtrack.add_trace(
    #             go.Scatter(
    #                 x=status_count_over_time['Date'], 
    #                 y=status_count_over_time['On-Track'], 
    #                 mode='lines', 
    #                 name='On-Track'
    #             )
    #         )
    #     if 'Off-Track' in status_count_over_time.columns:
    #         fig_offtrack.add_trace(
    #             go.Scatter(
    #                 x=status_count_over_time['Date'], 
    #                 y=status_count_over_time['Off-Track'], 
    #                 mode='lines', 
    #                 name='Off-Track'
    #             )
    #         )
    #     fig_offtrack.update_layout(
    #         title='On Track vs Off Track Over Time',
    #         xaxis_title='Date',
    #         yaxis_title='Count',
    #         legend_title='Status'
    #     )
    #     st.plotly_chart(fig_offtrack)

    #     mean_last_attendance_over_time = df_last_attendance.groupby('Date')['Days Since Last Attendance'].mean().reset_index()
    #     fig_last_attendance = px.line(mean_last_attendance_over_time, x='Date', y='Days Since Last Attendance', title='Average Days Since Last Attendance Over Time')
    #     st.plotly_chart(fig_last_attendance)

    #     mean_expertise_over_time = df_expertise_alignment.groupby('Date')['Coach Expertise'].mean().reset_index()
    #     fig_expertise = px.line(mean_expertise_over_time, x='Date', y='Coach Expertise', title='Average Coach Expertise Over Time')
    #     st.plotly_chart(fig_expertise)

    #     mean_alignment_over_time = df_expertise_alignment.groupby('Date')['Coach Alignment'].mean().reset_index()
    #     fig_alignment = px.line(mean_alignment_over_time, x='Date', y='Coach Alignment', title='Average Coach Alignment Over Time')
    #     st.plotly_chart(fig_alignment)

    #     # NPS Score
    #     mean_nps_over_time = df_nps.groupby('Date')['Apprentice NPS'].mean().reset_index()
    #     fig_nps = px.line(mean_nps_over_time, x='Date', y='Apprentice NPS', title='Average NPS Score Over Time')
    #     st.plotly_chart(fig_nps)
        
    # else:
    #     st.warning("No historical data found.")