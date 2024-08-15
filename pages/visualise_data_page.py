import streamlit as st
import pandas as pd
from pathlib import Path
import glob

def visualize_data_page():
    st.title("Historical Metrics Visualization")
    
    # Load all CSV files from the data directory
    data_path = Path("data")
    
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
    
        st.subheader("LM NPS Over Time")
        st.line_chart(df_lmnps.set_index('Date')['LM NPS'])

        st.subheader("LM ROI Over Time")
        st.line_chart(df_lmroi.set_index('Date')['LM ROI Out of 6'])

        st.subheader("Offtrack Status Over Time")
        df_offtrack_count = df_offtrack.groupby(['Date', 'Status']).size().unstack(fill_value=0)
        st.line_chart(df_offtrack_count)

        st.subheader("Days Since Last Attendance Over Time")
        st.line_chart(df_last_attendance.set_index('Date')['Days Since Last Attendance'])

        st.subheader("Coach Expertise Over Time")
        st.line_chart(df_expertise_alignment.set_index('Date')['Coach Expertise'])

        st.subheader("Coach Alignment Over Time")
        st.line_chart(df_expertise_alignment.set_index('Date')['Coach Alignment'])

        st.subheader("NPS Score Over Time")
        st.line_chart(df_nps.set_index('Date')['Apprentice NPS'])
        
    else:
        st.warning("No historical data found.")