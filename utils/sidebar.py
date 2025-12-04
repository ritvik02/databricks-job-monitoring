"""
Praxis Branded Sidebar for Databricks Job Monitor
Includes logo, navigation, controls, and status
"""

import streamlit as st
import base64
from pathlib import Path
from datetime import datetime
import os
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import Config


def render_logo():
    """Render Praxis logo in sidebar"""
    # Try multiple paths for the logo
    possible_paths = [
        Path(__file__).parent.parent / "assets" / "prax_logo_03.png",
        Path("./assets/prax_logo_03.png"),
        Path("/app/assets/prax_logo_03.png"),
    ]
    
    logo_data = None
    for logo_path in possible_paths:
        try:
            if logo_path.exists():
                with open(logo_path, "rb") as f:
                    logo_data = base64.b64encode(f.read()).decode()
                break
        except:
            continue
    
    if logo_data:
        st.markdown(f"""
        <div class="praxis-logo-container">
            <img src="data:image/png;base64,{logo_data}" 
                 alt="Praxis Logo" 
                 style="width: 200px; height: auto; margin-bottom: 0.75rem; 
                        display: block; margin-left: auto; margin-right: auto;">
            <div class="praxis-tagline">DARE FOR MORE ®</div>
            <div class="praxis-subtitle">Databricks Job<br/>Monitoring System</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback to text-based logo
        st.markdown("""
        <div class="praxis-logo-container">
            <div style="font-size: 2.2rem; font-weight: 900; color: white; 
                        letter-spacing: 0.15em; margin-bottom: 0.5rem;">
                PRAXIS
            </div>
            <div class="praxis-tagline">DARE FOR MORE ®</div>
            <div class="praxis-subtitle">Databricks Job<br/>Monitoring System</div>
        </div>
        """, unsafe_allow_html=True)


def render_sidebar(jobs, session_state):
    """
    Render the complete sidebar with logo, controls, and navigation
    
    Args:
        jobs: List of job configurations from config.yaml
        session_state: Streamlit session state object
    
    Returns:
        dict: Contains selected_job and other filter options
    """
    with st.sidebar:
        # Logo section
        render_logo()
        
        st.markdown("---")
        
        # Manual refresh button
        st.markdown("### 🔄 Controls")
        if st.button("🔄 Refresh Now", use_container_width=True, type="primary"):
            session_state.last_refresh = __import__('time').time()
            st.rerun()
        
        st.markdown("---")
        
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
                session_state.selected_job = None
            else:
                session_state.selected_job = selected
            
            st.markdown("---")
        
        # Auto-refresh toggle
        st.markdown("### ⏱️ Auto-Refresh")
        auto_refresh = st.toggle("Enable Auto-Refresh", value=session_state.auto_refresh)
        session_state.auto_refresh = auto_refresh
        
        if auto_refresh:
            refresh_interval = st.slider(
                "Refresh Interval (seconds)",
                min_value=10,
                max_value=300,
                value=session_state.refresh_interval,
                step=10
            )
            session_state.refresh_interval = refresh_interval
            
            # Show time until next refresh
            import time
            elapsed = time.time() - session_state.last_refresh
            remaining = max(0, refresh_interval - elapsed)
            st.info(f"⏱️ Next refresh in: {int(remaining)}s")
            
            # Auto-refresh logic
            if elapsed >= refresh_interval:
                session_state.last_refresh = time.time()
                st.rerun()
        
        st.markdown("---")
        
        # Connection status
        st.markdown("### 🔗 Connection")
        try:
            host = st.secrets.get("DATABRICKS_HOST")
            token = st.secrets.get("DATABRICKS_TOKEN")
        except:
            host = os.getenv('DATABRICKS_HOST')
            token = os.getenv('DATABRICKS_TOKEN')
        
        if host and token:
            st.markdown("""
            <div class="connection-status connection-connected">
                ✅ Connected
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"Host: {host[:40]}...")
        else:
            st.markdown("""
            <div class="connection-status connection-disconnected">
                ❌ Not configured
            </div>
            """, unsafe_allow_html=True)
            st.caption("Check your .env file")
        
        # Status Legend
        st.markdown("---")
        st.markdown("### 📖 Status Legend")
        st.markdown(f"""
        <div style="font-size: 0.85rem; line-height: 1.8;">
            <div>🔵 Running/Pending</div>
            <div>✅ Success</div>
            <div>❌ Failed</div>
            <div>🚫 Canceled</div>
            <div>⏱️ Timeout</div>
            <div>⚠️ Error/Terminating</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Last refresh time
        last_refresh_str = datetime.fromtimestamp(session_state.last_refresh).strftime("%H:%M:%S")
        st.markdown(f"""
        <div class="refresh-info">
            Last refreshed: {last_refresh_str}
        </div>
        """, unsafe_allow_html=True)
    
    return {
        'selected_job': session_state.selected_job,
        'auto_refresh': session_state.auto_refresh,
        'refresh_interval': session_state.refresh_interval
    }

