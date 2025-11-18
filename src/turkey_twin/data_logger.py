import csv, datetime
from typing import List, Dict, Any
class DataLogger:

    def __init__(self, vehicles: list):
        self.vehicles = vehicles
        self.filename = f"data/simulation_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.file = None
        self.writer = None
        self.header = []
        self.header = ['tick' , 'vehicle_id' ,'x','y','battery','status']

    def open_log(self):
        self.file = open(self.filename, 'w', newline='')
        self.writer = csv.writer(self.file) 
        self.writer.writerow(self.header)

    def close_log(self):
        if self.file:
            self.file.close()
            print('Logger closed')

    def log_state(self, tick: int):
        for vehicle in self.vehicles:
            line = [tick, vehicle.id, vehicle.location.x, vehicle.location.y, vehicle.battery_level, vehicle.status]
            self.writer.writerow(line)

        