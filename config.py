"""
Databricks Job Monitor - Configuration
Praxis Brand Colors and Application Settings
"""

import os
from pathlib import Path


class Config:
    """Application configuration"""
    
    # Praxis Brand Colors
    PRAXIS_BLACK = "#000000"
    PRAXIS_CYAN = "#00CECE"
    PRAXIS_BLUE = "#0EA5E9"
    PRAXIS_ORANGE = "#F97316"
    
    # Status Colors
    STATUS_SUCCESS = "#10B981"  # Green
    STATUS_FAILED = "#EF4444"   # Red
    STATUS_RUNNING = "#3B82F6"  # Blue
    STATUS_CANCELED = "#8B5CF6" # Purple
    STATUS_TIMEOUT = "#EC4899"  # Pink
    STATUS_WARNING = "#F59E0B"  # Orange
    STATUS_NEUTRAL = "#6B7280"  # Gray
    
    # Application Settings
    APP_TITLE = "Databricks Job Monitor"
    APP_SUBTITLE = "Monitor, trigger, and manage your Databricks jobs in real-time"
    APP_ICON = "🔄"
    
    # Default Settings
    DEFAULT_REFRESH_INTERVAL = 30  # seconds
    DEFAULT_RUN_HISTORY_LIMIT = 10
    
    # Timezone
    DISPLAY_TIMEZONE = "America/New_York"  # US Eastern Time
    
    # Paths - Auto-detect environment
    BASE_DIR = Path(__file__).parent
    ASSETS_DIR = BASE_DIR / "assets"
    
    # Thresholds for job health indicators (future use)
    THRESHOLD_HEALTHY_SUCCESS_RATE = 80
    THRESHOLD_WARNING_SUCCESS_RATE = 60

