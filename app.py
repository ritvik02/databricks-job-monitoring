"""
Praxis Databricks Job Monitoring System
Monitor, trigger, and manage Databricks jobs in real-time
"""

import streamlit as st
import os
import yaml
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import RunLifeCycleState, RunResultState
import pandas as pd

# Load environment variables from .env file (local development)
load_dotenv('.env')

# Import custom modules
from config import Config
from utils.styles import get_custom_css
from utils.sidebar import render_sidebar

# Page configuration
st.set_page_config(
    page_title=f"Praxis | {Config.APP_TITLE}",
    page_icon=Config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize session state
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
if 'refresh_interval' not in st.session_state:
    st.session_state.refresh_interval = Config.DEFAULT_REFRESH_INTERVAL
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()
if 'selected_job' not in st.session_state:
    st.session_state.selected_job = None


def load_config():
    """Load job configuration from config.yaml"""
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
            return config.get('jobs', [])
    except FileNotFoundError:
        st.error("❌ config.yaml not found. Please create it following the template.")
        return []
    except Exception as e:
        st.error(f"❌ Error loading config.yaml: {str(e)}")
        return []


def init_databricks_client():
    """Initialize Databricks workspace client"""
    try:
        # Try Streamlit secrets first (for deployed app), fall back to env vars (for local)
        try:
            host = st.secrets.get("DATABRICKS_HOST")
            token = st.secrets.get("DATABRICKS_TOKEN")
        except:
            host = os.getenv('DATABRICKS_HOST')
            token = os.getenv('DATABRICKS_TOKEN')
        
        if not host or not token:
            st.error("❌ Missing Databricks credentials. Please set DATABRICKS_HOST and DATABRICKS_TOKEN in your .env file.")
            st.info("💡 Copy env.example to .env and fill in your credentials.")
            return None
        
        client = WorkspaceClient(host=host, token=token)
        return client
    except Exception as e:
        st.error(f"❌ Failed to initialize Databricks client: {str(e)}")
        return None


def get_job_details(client, job_id):
    """Get job details by ID"""
    try:
        job = client.jobs.get(job_id=job_id)
        return job
    except Exception as e:
        st.error(f"❌ Error fetching job {job_id}: {str(e)}")
        return None


def get_job_runs(client, job_id, limit=10):
    """Get the last N runs for a job"""
    try:
        runs = client.jobs.list_runs(job_id=job_id, limit=limit, expand_tasks=False)
        return list(runs)
    except Exception as e:
        st.error(f"❌ Error fetching runs for job {job_id}: {str(e)}")
        return []


def trigger_job_run(client, job_id):
    """Trigger a new job run"""
    try:
        run = client.jobs.run_now(job_id=job_id)
        return run
    except Exception as e:
        st.error(f"❌ Error triggering job {job_id}: {str(e)}")
        return None


def cancel_job_run(client, run_id):
    """Cancel a running job"""
    try:
        client.jobs.cancel_run(run_id=run_id)
        return True
    except Exception as e:
        st.error(f"❌ Error cancelling run {run_id}: {str(e)}")
        return False


def get_status_info(state, result_state=None):
    """Get status display information (emoji, color, text, css_class)"""
    if state == RunLifeCycleState.RUNNING or state == RunLifeCycleState.PENDING:
        return "🔵", Config.STATUS_RUNNING, "RUNNING", "status-running"
    elif state == RunLifeCycleState.TERMINATING:
        return "⚠️", Config.STATUS_WARNING, "TERMINATING", "status-warning"
    elif state == RunLifeCycleState.TERMINATED:
        if result_state == RunResultState.SUCCESS:
            return "✅", Config.STATUS_SUCCESS, "SUCCESS", "status-success"
        elif result_state == RunResultState.FAILED:
            return "❌", Config.STATUS_FAILED, "FAILED", "status-failed"
        elif result_state == RunResultState.CANCELED:
            return "🚫", Config.STATUS_CANCELED, "CANCELED", "status-canceled"
        elif result_state == RunResultState.TIMEDOUT:
            return "⏱️", Config.STATUS_TIMEOUT, "TIMEOUT", "status-timeout"
        else:
            return "⚪", Config.STATUS_NEUTRAL, "TERMINATED", "status-neutral"
    elif state == RunLifeCycleState.SKIPPED:
        return "⏭️", Config.STATUS_WARNING, "SKIPPED", "status-warning"
    elif state == RunLifeCycleState.INTERNAL_ERROR:
        return "⚠️", Config.STATUS_FAILED, "ERROR", "status-failed"
    else:
        return "⚪", Config.STATUS_NEUTRAL, str(state), "status-neutral"


def format_timestamp(ts_ms):
    """Format timestamp from milliseconds to readable format in configured timezone"""
    if ts_ms:
        # Convert from UTC timestamp to timezone-aware datetime
        utc_dt = datetime.fromtimestamp(ts_ms / 1000, tz=ZoneInfo("UTC"))
        # Convert to display timezone
        local_dt = utc_dt.astimezone(ZoneInfo(Config.DISPLAY_TIMEZONE))
        return local_dt.strftime("%Y-%m-%d %H:%M:%S")
    return "N/A"


def calculate_duration(start_ms, end_ms):
    """Calculate duration in human-readable format"""
    if start_ms and end_ms:
        duration_sec = (end_ms - start_ms) / 1000
        if duration_sec < 60:
            return f"{int(duration_sec)}s"
        elif duration_sec < 3600:
            return f"{int(duration_sec / 60)}m {int(duration_sec % 60)}s"
        else:
            hours = int(duration_sec / 3600)
            minutes = int((duration_sec % 3600) / 60)
            return f"{hours}h {minutes}m"
    return "N/A"


def display_job_card(client, job_config):
    """Display a job monitoring card with Praxis styling"""
    job_id = job_config['job_id']
    display_name = job_config.get('display_name', f'Job {job_id}')
    
    # Get job details
    job = get_job_details(client, job_id)
    if not job:
        return
    
    # Get job runs
    runs = get_job_runs(client, job_id, limit=Config.DEFAULT_RUN_HISTORY_LIMIT)
    
    # Determine status for card styling
    card_class = "job-card"
    if runs and len(runs) > 0:
        latest_run = runs[0]
        emoji, color, status_text, css_class = get_status_info(
            latest_run.state.life_cycle_state,
            latest_run.state.result_state
        )
        if status_text == "SUCCESS":
            card_class += " job-card-success"
        elif status_text == "FAILED":
            card_class += " job-card-failed"
        elif status_text == "RUNNING":
            card_class += " job-card-running"
    
    # Determine if this job should be expanded
    is_expanded = (st.session_state.selected_job is None or 
                   st.session_state.selected_job == display_name)
    
    # Create expandable section for each job
    with st.expander(f"📊 **{display_name}**", expanded=is_expanded):
        # Job overview section - compact layout
        # Check if cancel button should be shown
        show_cancel = False
        if runs and len(runs) > 0:
            latest_run = runs[0]
            if latest_run.state.life_cycle_state in [RunLifeCycleState.RUNNING, RunLifeCycleState.PENDING]:
                show_cancel = True
        
        # Use 3 columns if no cancel button, 4 if cancel button needed
        if show_cancel:
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
        else:
            col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            st.markdown(f"**Job Name:** {job.settings.name}")
            st.caption(f"Job ID: {job_id}")
        
        with col2:
            if runs and len(runs) > 0:
                latest_run = runs[0]
                emoji, color, status_text, css_class = get_status_info(
                    latest_run.state.life_cycle_state,
                    latest_run.state.result_state
                )
                st.markdown(f'**Latest Status:** <span class="status-badge {css_class}">{emoji} {status_text}</span>', unsafe_allow_html=True)
            else:
                st.markdown("**Latest Status:** No runs found")
        
        with col3:
            if st.button("▶️ Trigger", key=f"trigger_{job_id}", use_container_width=True):
                with st.spinner("Triggering job..."):
                    result = trigger_job_run(client, job_id)
                    if result:
                        st.success(f"✅ Job triggered! Run ID: {result.run_id}")
                        time.sleep(1)
                        st.rerun()
        
        if show_cancel:
            with col4:
                if st.button("⏹️ Cancel", key=f"cancel_{runs[0].run_id}", use_container_width=True):
                    with st.spinner("Cancelling run..."):
                        if cancel_job_run(client, runs[0].run_id):
                            st.success("✅ Run cancelled!")
                            time.sleep(1)
                            st.rerun()
        
        # Run history section
        st.markdown(f'<div class="sub-header-compact">Run History (Last {Config.DEFAULT_RUN_HISTORY_LIMIT})</div>', unsafe_allow_html=True)
        
        if runs and len(runs) > 0:
            run_data = []
            for run in runs:
                emoji, color, status_text, css_class = get_status_info(
                    run.state.life_cycle_state,
                    run.state.result_state
                )
                
                run_data.append({
                    "Status": f"{emoji} {status_text}",
                    "Run ID": run.run_id,
                    "Start Time": format_timestamp(run.start_time),
                    "End Time": format_timestamp(run.end_time) if run.end_time else "Running",
                    "Duration": calculate_duration(run.start_time, run.end_time) if run.end_time else "In Progress",
                    "Run Page URL": run.run_page_url
                })
            
            df = pd.DataFrame(run_data)
            
            # Display as scrollable table showing 4 rows at a time
            st.dataframe(
                df,
                column_config={
                    "Run Page URL": st.column_config.LinkColumn("Run Page URL", display_text="View in Databricks")
                },
                hide_index=True,
                use_container_width=True,
                height=220  # Shows ~4 rows with scrolling
            )
        else:
            st.info("No run history available for this job.")


def main():
    """Main application"""
    # Load job configuration early for sidebar
    jobs = load_config()
    
    # Render sidebar and get filters
    filters = render_sidebar(jobs, st.session_state)
    
    # Main content area
    st.markdown(f'<div class="main-header">{Config.APP_ICON} {Config.APP_TITLE}</div>', unsafe_allow_html=True)
    st.markdown(f'<p class="main-subtitle">{Config.APP_SUBTITLE}</p>', unsafe_allow_html=True)
    
    # Initialize client
    client = init_databricks_client()
    if not client:
        st.warning("⚠️ Please configure your Databricks credentials to continue.")
        st.code("""
# Steps to configure:
1. Copy env.example to .env
2. Fill in your DATABRICKS_HOST and DATABRICKS_TOKEN
3. Refresh this page
        """)
        return
    
    # Check if jobs are configured
    if not jobs:
        st.warning("⚠️ No jobs configured. Please add jobs to config.yaml")
        st.code("""
# Example config.yaml:
jobs:
  - job_id: 123456789
    display_name: "My ETL Job"
  - job_id: 987654321
    display_name: "My Report Job"
        """)
        return
    
    # Display summary metrics
    st.markdown('<div class="sub-header">📈 Overview</div>', unsafe_allow_html=True)
    
    # Calculate metrics
    total_jobs = len(jobs)
    
    # Quick stats row
    metric_cols = st.columns(4)
    with metric_cols[0]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_jobs}</div>
            <div class="metric-label">Jobs Monitored</div>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_cols[1]:
        tz_name = Config.DISPLAY_TIMEZONE.split('/')[-1].replace('_', ' ')
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{tz_name}</div>
            <div class="metric-label">Timezone</div>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_cols[2]:
        refresh_status = "ON" if st.session_state.auto_refresh else "OFF"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{refresh_status}</div>
            <div class="metric-label">Auto-Refresh</div>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_cols[3]:
        interval = st.session_state.refresh_interval if st.session_state.auto_refresh else "-"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{interval}s</div>
            <div class="metric-label">Refresh Interval</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display job cards
    st.markdown('<div class="sub-header">📋 Job Details</div>', unsafe_allow_html=True)
    
    for job_config in jobs:
        display_job_card(client, job_config)
    
    # Auto-refresh placeholder to trigger rerun
    if st.session_state.auto_refresh:
        time.sleep(0.1)


if __name__ == "__main__":
    main()
