# datatrac/core/config.py
import os
from pathlib import Path

# --- LOCAL CONFIGURATION ---
# Base directory for local app data (e.g., downloaded files, temp items)
APP_DIR = Path(os.getenv("DATATRAC_HOME", Path.home() / ".datatrac"))

# --- CENTRAL DATABASE CONFIGURATION (PostgreSQL) ---
DB_USER = "datatrac_user"
# IMPORTANT: For security, use environment variables in a real project
# e.g., os.getenv("DB_PASSWORD", "your_strong_password")
DB_PASSWORD = "your_strong_password"
DB_HOST = "taklu.chickenkiller.com"
DB_NAME = "datatrac_db"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# --- REMOTE REGISTRY CONFIGURATION ---
REMOTE_USER = "naruto"
REMOTE_HOST = "taklu.chickenkiller.com"
REMOTE_STORAGE_PATH = "/home/naruto/datasets"

REMOTE_TARGET = f"{REMOTE_USER}@{REMOTE_HOST}"

# Ensure the local app directory exists
APP_DIR.mkdir(exist_ok=True)    