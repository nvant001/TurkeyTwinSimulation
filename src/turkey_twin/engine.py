# src/turkey_twin/engine.py
import datetime
from turkey_twin.entities import Vehicle, Warehouse
from turkey_twin.data_logger import DataLogger

class SimulationEngine:
    def __init__(self):
        self.time = 0
        self.vehicles: list[Vehicle] = []
        self.warehouses: list[Warehouse] = []
        self.logger = None

    def add_vehicle(self, vehicle: Vehicle):
        self.vehicles.append(vehicle)
        print(f"[{datetime.datetime.now()}]: Vehicle {vehicle.id} added.")

    def initialize_logger(self):
        """Initialize logger for persistent API usage"""
        self.logger = DataLogger(self.vehicles)
        self.logger.open_log()

    def step(self, log_to_db: bool = False):
        self.time += 1
        
        # 1. Update Physics
        for vehicle in self.vehicles:
            vehicle.update()
        
        # 2. Log Data (Fixes the issue where API wasn't saving data)
        if log_to_db and self.logger:
            self.logger.log_state(self.time)
        elif log_to_db and not self.logger:
            print("[ENGINE] Warning: specific log requested but logger not initialized.")

    def run_batch(self, steps: int):
        """Used for CLI batch runs (main.py)"""
        self.initialize_logger()
        self.logger.clear_log() # Start fresh for batch runs
        
        try: 
            self.logger.log_state(tick=0)
            for _ in range(steps):
                self.step(log_to_db=True)
                print(f"[{datetime.datetime.now()}]: Batch Step {self.time}")
        finally:
            self.logger.close_log()