import streamlit as st
import os
import yaml
import time
from datetime import datetime
from dotenv import load_dotenv
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import RunLifeCycleState, RunResultState
import pandas as pd

# Load environment variables from .env file (local development)
load_dotenv('.env')

# Page configuration
st.set_page_config(
    page_title="Databricks Job Monitor",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
if 'refresh_interval' not in st.session_state:
    st.session_state.refresh_interval = 30
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
    """Get status display information (emoji, color, text)"""
    if state == RunLifeCycleState.RUNNING or state == RunLifeCycleState.PENDING:
        return "🔵", "#1f77b4", "RUNNING"
    elif state == RunLifeCycleState.TERMINATING:
        return "⚠️", "#ff7f0e", "TERMINATING"
    elif state == RunLifeCycleState.TERMINATED:
        if result_state == RunResultState.SUCCESS:
            return "✅", "#2ca02c", "SUCCESS"
        elif result_state == RunResultState.FAILED:
            return "❌", "#d62728", "FAILED"
        elif result_state == RunResultState.CANCELED:
            return "🚫", "#9467bd", "CANCELED"
        elif result_state == RunResultState.TIMEDOUT:
            return "⏱️", "#e377c2", "TIMEOUT"
        else:
            return "⚪", "#7f7f7f", "TERMINATED"
    elif state == RunLifeCycleState.SKIPPED:
        return "⏭️", "#bcbd22", "SKIPPED"
    elif state == RunLifeCycleState.INTERNAL_ERROR:
        return "⚠️", "#d62728", "ERROR"
    else:
        return "⚪", "#7f7f7f", str(state)


def format_timestamp(ts_ms):
    """Format timestamp from milliseconds to readable format"""
    if ts_ms:
        dt = datetime.fromtimestamp(ts_ms / 1000)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
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
    """Display a job monitoring card"""
    job_id = job_config['job_id']
    display_name = job_config.get('display_name', f'Job {job_id}')
    
    # Get job details
    job = get_job_details(client, job_id)
    if not job:
        return
    
    # Get job runs
    runs = get_job_runs(client, job_id, limit=10)
    
    # Determine if this job should be expanded
    is_expanded = (st.session_state.selected_job is None or 
                   st.session_state.selected_job == display_name)
    
    # Create expandable section for each job
    with st.expander(f"📊 **{display_name}**", expanded=is_expanded):
        # Job overview section
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        
        with col1:
            st.markdown(f"**Job Name:** {job.settings.name}")
        
        with col2:
            if runs and len(runs) > 0:
                latest_run = runs[0]
                emoji, color, status_text = get_status_info(
                    latest_run.state.life_cycle_state,
                    latest_run.state.result_state
                )
                st.markdown(f"**Latest Status:** {emoji} {status_text}")
            else:
                st.markdown("**Latest Status:** No runs found")
        
        with col3:
            if st.button("▶️ Trigger Run", key=f"trigger_{job_id}"):
                with st.spinner("Triggering job..."):
                    result = trigger_job_run(client, job_id)
                    if result:
                        st.success(f"✅ Job triggered! Run ID: {result.run_id}")
                        time.sleep(1)
                        st.rerun()
        
        with col4:
            # Show cancel button only if there's a running job
            if runs and len(runs) > 0:
                latest_run = runs[0]
                if latest_run.state.life_cycle_state in [RunLifeCycleState.RUNNING, RunLifeCycleState.PENDING]:
                    if st.button("⏹️ Cancel", key=f"cancel_{latest_run.run_id}"):
                        with st.spinner("Cancelling run..."):
                            if cancel_job_run(client, latest_run.run_id):
                                st.success("✅ Run cancelled!")
                                time.sleep(1)
                                st.rerun()
        
        st.divider()
        
        # Run history section
        st.markdown("### Run History (Last 10)")
        
        if runs and len(runs) > 0:
            run_data = []
            for run in runs:
                emoji, color, status_text = get_status_info(
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
                    "Run Page URL": st.column_config.LinkColumn("Run Page URL")
                },
                hide_index=True,
                use_container_width=True,
                height=220  # Shows ~4 rows with scrolling
            )
        else:
            st.info("No run history available for this job.")


def main():
    """Main application"""
    st.title("🔄 Databricks Job Monitor")
    st.markdown("Monitor, trigger, and manage your Databricks jobs in real-time")
    
    # Load job configuration early for sidebar
    jobs = load_config()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Controls")
        
        # Manual refresh button
        if st.button("🔄 Refresh Now", use_container_width=True):
            st.session_state.last_refresh = time.time()
            st.rerun()
        
        st.divider()
        
        # Job Navigation
        if jobs and len(jobs) > 0:
            st.markdown("### 📋 Jobs")
            job_names = ["All Jobs"] + [job.get('display_name', f"Job {job['job_id']}") for job in jobs]
            
            selected = st.radio(
                "Select a job to navigate:",
                job_names,
                index=0,
                label_visibility="collapsed"
            )
            
            if selected == "All Jobs":
                st.session_state.selected_job = None
            else:
                st.session_state.selected_job = selected
            
            st.divider()
        
        # Auto-refresh toggle
        st.markdown("### Auto-Refresh")
        auto_refresh = st.toggle("Enable Auto-Refresh", value=st.session_state.auto_refresh)
        st.session_state.auto_refresh = auto_refresh
        
        if auto_refresh:
            refresh_interval = st.slider(
                "Refresh Interval (seconds)",
                min_value=10,
                max_value=300,
                value=st.session_state.refresh_interval,
                step=10
            )
            st.session_state.refresh_interval = refresh_interval
            
            # Show time until next refresh
            elapsed = time.time() - st.session_state.last_refresh
            remaining = max(0, refresh_interval - elapsed)
            st.info(f"⏱️ Next refresh in: {int(remaining)}s")
            
            # Auto-refresh logic
            if elapsed >= refresh_interval:
                st.session_state.last_refresh = time.time()
                st.rerun()
        
        st.divider()
        
        # Connection status
        st.markdown("### Connection Status")
        try:
            host = st.secrets.get("DATABRICKS_HOST")
            token = st.secrets.get("DATABRICKS_TOKEN")
        except:
            host = os.getenv('DATABRICKS_HOST')
            token = os.getenv('DATABRICKS_TOKEN')
        
        if host and token:
            st.success("✅ Connected")
            st.caption(f"Host: {host}")
        else:
            st.error("❌ Not configured")
            st.caption("Check your .env file")
        
        st.divider()
        
        # Last refresh time
        last_refresh_str = datetime.fromtimestamp(st.session_state.last_refresh).strftime("%H:%M:%S")
        st.caption(f"Last refreshed: {last_refresh_str}")
    
    # Main content
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
    
    # Display job cards
    for job_config in jobs:
        display_job_card(client, job_config)
        st.markdown("---")
    
    # Auto-refresh placeholder to trigger rerun
    if st.session_state.auto_refresh:
        time.sleep(0.1)


if __name__ == "__main__":
    main()

