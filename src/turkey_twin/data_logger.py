import csv, datetime
from typing import List, Dict, Any
import sqlite3

DATABASE_NAME = 'data/simulation_data.db'
class DataLogger:

    def __init__(self, vehicles: list):
        self.vehicles = vehicles
        # self.filename = f"data/simulation_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        # self.file = None
        # self.writer = None
        # self.header = []
        # self.header = ['tick' , 'vehicle_id' ,'x','y','battery','status']

        self.conn: sqlite3.Connection = None
        self.cursor: sqlite3.Cursor = None

        self.scheme = """
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
        # self.file = open(self.filename, 'w', newline='')
        # self.writer = csv.writer(self.file) 
        # self.writer.writerow(self.header)
        try:
            self.conn = sqlite3.connect(DATABASE_NAME)
            self.cursor = self.conn.cursor()

            self.cursor.execute(self.scheme)
            self.conn.commit()
            print('Database connected and table verified')
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def close_log(self):
        # if self.file:
        #     self.file.close()
        if self.conn:
            self.conn.close()
            print('Database connection closed')

    def log_state(self, tick: int):
        data_to_insert = []
        for vehicle in self.vehicles:
            # line = [tick, vehicle.id, vehicle.location.x, vehicle.location.y, vehicle.battery_level, vehicle.status]
            # self.writer.writerow(line)
            line = (tick, vehicle.id, vehicle.location.x, vehicle.location.y, vehicle.battery_level, vehicle.status)
            data_to_insert.append(line)
        
        self.cursor.executemany(self.insert_query, data_to_insert)
        self.conn.commit()
        