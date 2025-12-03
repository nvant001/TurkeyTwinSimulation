# src/turkey_twin/data_logger.py
import sqlite3
from typing import List
from turkey_twin.config import DATABASE_PATH

class DataLogger:
    def __init__(self, vehicles: list):
        self.vehicles = vehicles
        self.conn = None
        self.cursor = None

        self.schema = """
        CREATE TABLE IF NOT EXISTS simulation_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tick INTEGER NOT NULL,
            vehicle_id TEXT NOT NULL,
            x REAL,
            y REAL,
            battery REAL,
            status TEXT
        );"""

        self.insert_query = """
        INSERT INTO simulation_records (tick, vehicle_id, x, y, battery, status)
        VALUES (?, ?, ?, ?, ?, ?);
        """

    def open_log(self):
        try:
            self.conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.cursor.execute(self.schema)
            self.conn.commit()
            print(f'[LOGGER] Connected to database at {DATABASE_PATH}')
        except sqlite3.Error as e:
            print(f"[LOGGER] Database error: {e}")

    def clear_log(self):
        """Clears previous simulation data for a fresh run."""
        if self.cursor:
            self.cursor.execute("DELETE FROM simulation_records")
            self.conn.commit()
            print("[LOGGER] Database cleared.")

    def close_log(self):
        if self.conn:
            self.conn.close()
            print('[LOGGER] Database connection closed')

    def log_state(self, tick: int):
        if not self.conn:
            print("[LOGGER] Error: Attempted to log to closed database.")
            return

        data_to_insert = []
        for vehicle in self.vehicles:
            line = (tick, vehicle.id, vehicle.location.x, vehicle.location.y, vehicle.battery_level, vehicle.status)
            data_to_insert.append(line)
        
        try:
            self.cursor.executemany(self.insert_query, data_to_insert)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"[LOGGER] Write error: {e}")