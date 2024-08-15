import streamlit as st
import pandas as pd
from pathlib import Path
import glob
import plotly.express as px 
import plotly.graph_objects as go  # Import Plotly graph_objects

def visualize_data_page():
    st.title("Historical Metrics Visualization")
    
    # Load all CSV files from the data directory
    data_path = Path("anonymised_csv_files")
    
    if data_path.exists():
        lmnps_files = glob.glob(str(data_path / "df_lmnps_*.csv"))
        lmroi_files = glob.glob(str(data_path / "df_lmroi_*.csv"))
        offtrack_files = glob.glob(str(data_path / "df_offtrack_*.csv"))
        last_attendance_files = glob.glob(str(data_path / "df_last_attendance_*.csv"))
        expertise_alignment_files = glob.glob(str(data_path / "df_expertise_alignment_*.csv"))
        nps_files = glob.glob(str(data_path / "df_nps_*.csv"))
        
        df_lmnps = pd.concat((pd.read_csv(f) for f in lmnps_files), ignore_index=True)
        df_lmroi = pd.concat((pd.read_csv(f) for f in lmroi_files), ignore_index=True)
        df_offtrack = pd.concat((pd.read_csv(f) for f in offtrack_files), ignore_index=True)
        df_last_attendance = pd.concat((pd.read_csv(f) for f in last_attendance_files), ignore_index=True)
        df_expertise_alignment = pd.concat((pd.read_csv(f) for f in expertise_alignment_files), ignore_index=True)
        df_nps = pd.concat((pd.read_csv(f) for f in nps_files), ignore_index=True)
        st.write("LM NPS Historical Data", df_lmnps)
        st.write("LM ROI Historical Data", df_lmroi)
        st.write("Offtrack Historical Data", df_offtrack)
        st.write("Last Attendance Historical Data", df_last_attendance)
        st.write("Coach Expertise and Alignment Historical Data", df_expertise_alignment)
        st.write("NPS Score Historical Data", df_nps)
        
        # Visualizations
        
        mean_lmnps_over_time = df_lmnps.groupby('Date')['LM NPS'].mean().reset_index()

        # Create Plotly line chart
        fig = px.line(mean_lmnps_over_time, x='Date', y='LM NPS', title='Average NPS Score Over Time')
        
        # Display the Plotly chart in Streamlit
        st.plotly_chart(fig)

        mean_lmroi_over_time = df_lmroi.groupby('Date')['LM ROI Out of 6'].mean().reset_index()
        fig_lmroi = px.line(mean_lmroi_over_time, x='Date', y='LM ROI Out of 6', title='Average LM ROI Score Over Time')
        st.plotly_chart(fig_lmroi)

        # Offtrack Status: Calculate the count of "On Track" and "Offtrack" status for each date
        status_count_over_time = df_offtrack.groupby(['Date', 'Status']).size().unstack(fill_value=0).reset_index()
        
        # Inspect the DataFrame's contents
        st.write(status_count_over_time)

        # Create the line graph
        fig_offtrack = go.Figure()
        if 'On-Track' in status_count_over_time.columns:
            fig_offtrack.add_trace(
                go.Scatter(
                    x=status_count_over_time['Date'], 
                    y=status_count_over_time['On-Track'], 
                    mode='lines', 
                    name='On-Track'
                )
            )
        if 'Off-Track' in status_count_over_time.columns:
            fig_offtrack.add_trace(
                go.Scatter(
                    x=status_count_over_time['Date'], 
                    y=status_count_over_time['Off-Track'], 
                    mode='lines', 
                    name='Off-Track'
                )
            )
        fig_offtrack.update_layout(
            title='On Track vs Off Track Over Time',
            xaxis_title='Date',
            yaxis_title='Count',
            legend_title='Status'
        )
        st.plotly_chart(fig_offtrack)

        mean_last_attendance_over_time = df_last_attendance.groupby('Date')['Days Since Last Attendance'].mean().reset_index()
        fig_last_attendance = px.line(mean_last_attendance_over_time, x='Date', y='Days Since Last Attendance', title='Average Days Since Last Attendance Over Time')
        st.plotly_chart(fig_last_attendance)

        mean_expertise_over_time = df_expertise_alignment.groupby('Date')['Coach Expertise'].mean().reset_index()
        fig_expertise = px.line(mean_expertise_over_time, x='Date', y='Coach Expertise', title='Average Coach Expertise Over Time')
        st.plotly_chart(fig_expertise)

        mean_alignment_over_time = df_expertise_alignment.groupby('Date')['Coach Alignment'].mean().reset_index()
        fig_alignment = px.line(mean_alignment_over_time, x='Date', y='Coach Alignment', title='Average Coach Alignment Over Time')
        st.plotly_chart(fig_alignment)

        # NPS Score
        mean_nps_over_time = df_nps.groupby('Date')['Apprentice NPS'].mean().reset_index()
        fig_nps = px.line(mean_nps_over_time, x='Date', y='Apprentice NPS', title='Average NPS Score Over Time')
        st.plotly_chart(fig_nps)
        
    else:
        st.warning("No historical data found.")