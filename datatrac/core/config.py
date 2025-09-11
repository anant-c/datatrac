# datatrac/core/config.py
import os
from pathlib import Path

# --- LOCAL CONFIGURATION ---
# Base directory for the application's local data (like the database)
APP_DIR = Path(os.getenv("DATATRAC_HOME", Path.home() / ".datatrac"))
# Path to the SQLite database
DATABASE_URL = f"sqlite:///{APP_DIR / 'datatrac.db'}"

# --- REMOTE REGISTRY CONFIGURATION ---
REMOTE_USER = "naruto"
REMOTE_HOST = "taklu.chickenkiller.com"
REMOTE_STORAGE_PATH = "/home/naruto/datasets"

# Helper to format the full SSH target address
REMOTE_TARGET = f"{REMOTE_USER}@{REMOTE_HOST}"

# Ensure the local app directory exists
APP_DIR.mkdir(exist_ok=True)