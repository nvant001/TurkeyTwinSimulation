# src/turkey_twin/utils.py
import sqlite3
import pandas as pd
import numpy as np
import os
import streamlit as st # Keep this if you want to keep using @st.cache_data, otherwise remove
from turkey_twin.config import DATABASE_PATH    

# NOTE: If you remove streamlit import, remove the @st.cache_data decorators below.
# For this utility file, it's often cleaner to remove Streamlit dependencies if possible, 
# but for simplicity, we can keep them if this file is primarily for the dashboard.
# Ideally, "reporter.py" shouldn't depend on streamlit, so let's make a plain version.

def load_data_pure() -> pd.DataFrame:
    """Reads data without Streamlit caching (for the reporter script)."""
    if not os.path.exists(DATABASE_PATH):
        print(f"Database not found at {DATABASE_PATH}")
        return pd.DataFrame()
        
    conn = sqlite3.connect(DATABASE_PATH)
    df = pd.read_sql("SELECT * FROM simulation_records ORDER BY tick DESC", conn)
    conn.close()
    return df

def calculate_kpis_pure(df: pd.DataFrame) -> dict:
    """Calculates KPIs without Streamlit caching."""
    if df.empty:
        return {'avg_battery': 0, 'total_distance': 0, 'utilization_ratio': 0}

    # 1. Avg Battery
    latest_tick = df['tick'].max()
    latest_tick_df = df[df['tick'] == latest_tick]
    avg_battery = latest_tick_df['battery'].mean()

    # 2. Total Distance
    df_copy = df.copy()
    df_copy['prev_x'] = df_copy.groupby('vehicle_id')['x'].shift(1)
    df_copy['prev_y'] = df_copy.groupby('vehicle_id')['y'].shift(1)
    df_moved = df_copy.dropna(subset=['prev_x', 'prev_y']).copy()
    
    df_moved['distance'] = np.sqrt(
        (df_moved['x'] - df_moved['prev_x'])**2 + 
        (df_moved['y'] - df_moved['prev_y'])**2
    )
    total_distance = df_moved['distance'].sum()

    # 3. Utilization
    total_records = len(df)
    moving_records = df[df['status'] == 'MOVING'].shape[0]
    utilization_ratio = (moving_records / total_records) * 100 if total_records > 0 else 0

    return {
        'avg_battery': avg_battery,
        'total_distance': total_distance,
        'utilization_ratio': utilization_ratio
    }