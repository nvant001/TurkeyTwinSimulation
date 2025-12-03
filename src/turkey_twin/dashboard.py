# src/turkey_twin/dashboard.py
import streamlit as st
import sqlite3
import pandas as pd
import requests
import os
import numpy as np
import plotly.express as px
from turkey_twin.config import DATABASE_PATH 

API_URL = "http://localhost:8000"
DEFAULT_STEPS = 5

WAREHOUSE_DATA = pd.DataFrame({
    'x': [1, 9], 'y': [1, 9],
    'id': ['WH-001 (Start)', 'WH-002 (End)'],
    'status': ['Warehouse', 'Warehouse'],
    'battery': [100.0, 100.0]
})

@st.cache_data(ttl=2) 
def load_data_from_db():
    if not os.path.exists(DATABASE_PATH):
        return pd.DataFrame()
        
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        df = pd.read_sql("SELECT * FROM simulation_records ORDER BY tick DESC", conn)
    except pd.errors.DatabaseError:
        df = pd.DataFrame() # Handle empty/locked DB gracefully
    finally:
        conn.close()
    return df

@st.cache_data(ttl=2)
def calculate_kpis(df: pd.DataFrame) -> dict:
    if df.empty:
        return {'avg_battery': 0, 'total_distance': 0, 'utilization_ratio': 0}
    
    latest_tick = df['tick'].max()
    latest_tick_df = df[df['tick'] == latest_tick]
    avg_battery = latest_tick_df['battery'].mean()

    df_copy = df.copy()
    df_copy['prev_x'] = df_copy.groupby('vehicle_id')['x'].shift(1)
    df_copy['prev_y'] = df_copy.groupby('vehicle_id')['y'].shift(1)
    df_moved = df_copy.dropna(subset=['prev_x', 'prev_y']).copy()
    
    df_moved['distance'] = np.sqrt(
        (df_moved['x'] - df_moved['prev_x'])**2 + 
        (df_moved['y'] - df_moved['prev_y'])**2
    )
    
    return {
        'avg_battery': avg_battery,
        'total_distance': df_moved['distance'].sum(),
        'utilization_ratio': (df[df['status'] == 'MOVING'].shape[0] / len(df) * 100)
    }

def call_api(endpoint):
    try:
        requests.post(f"{API_URL}{endpoint}")
        st.cache_data.clear() # Force refresh
        st.rerun()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")

def main():
    st.set_page_config(layout="wide", page_title="TurkeyTwin Dashboard")
    st.title("TurkeyTwin Simulation Digital Dashboard 🦃")

    with st.sidebar:
        st.header("Simulation Control")
        steps = st.number_input("Steps:", min_value=1, value=DEFAULT_STEPS)
        
        if st.button("▶️ Advance Simulation"):
            call_api(f"/control/step/{steps}")
            
        if st.button("⏮️ Reset Simulation"):
            call_api("/control/reset")
            
        st.markdown("---")
        if st.button("🔄 Refresh Data Only"):
            st.cache_data.clear()
            st.rerun()

    data_df = load_data_from_db()

    if not data_df.empty:
        kpis = calculate_kpis(data_df)
        latest_tick = data_df['tick'].max()
        
        st.header("Key Performance Indicators")
        c1, c2, c3 = st.columns(3)
        c1.metric("Fleet Avg Battery", f"{kpis['avg_battery']:.1f}%")
        c2.metric("Total Distance", f"{kpis['total_distance']:.2f}")
        c3.metric("Utilization", f"{kpis['utilization_ratio']:.1f}%")
        
        st.markdown("---")
        st.subheader(f"Live Map (Tick {latest_tick})")
        
        live_df = data_df[data_df['tick'] == latest_tick].copy()
        if 'id' in live_df.columns:
            live_df = live_df.drop(columns=['id'])
            
       
        live_df = live_df.rename(columns={'vehicle_id': 'id'})
        
        # Merge vehicles with static warehouses for plotting
        plot_df = pd.concat([live_df[['x','y','id','status','battery']], WAREHOUSE_DATA], ignore_index=True)

        fig = px.scatter(plot_df, x="x", y="y", color="status", symbol="status", 
                         text="id", hover_data=["battery"], height=600, size_max=15)
        fig.update_xaxes(range=[-1, 11], dtick=1)
        fig.update_yaxes(range=[-1, 11], dtick=1, scaleanchor="x", scaleratio=1)
        st.plotly_chart(fig, width='stretch')
        
        with st.expander("View Raw Data Log"):
            st.dataframe(data_df.head(100))
    else:
        st.info("Simulation database is empty. Click 'Reset' or 'Advance' to generate data.")

if __name__ == "__main__":
    main()