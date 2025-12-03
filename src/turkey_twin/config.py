# src/turkey_twin/config.py
import os
from pathlib import Path

# Get the project root directory (assuming this file is in src/turkey_twin/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_PATH = DATA_DIR / "simulation_data.db"
LOG_DIR = BASE_DIR / "logs"