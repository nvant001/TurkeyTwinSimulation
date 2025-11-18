from entities import Vehicle, Warehouse, Location
import datetime
import csv
from data_logger import DataLogger
class SimulationEngine:
    def __init__(self):
        self.time = 0
        self.vehicles: list[Vehicle] = []
        self.warehouses: list[Warehouse] = []

    def add_vehicle(self, vehicle: Vehicle):
        self.vehicles.append(vehicle)
        print(f"[{datetime.datetime.now()}]: Vehicle {vehicle.id} added to simulation.")

    def step(self):
        self.time += 1
        print(f"[{datetime.datetime.now()}]: Simulation time step {self.time}")
        for vehicle in self.vehicles:
            vehicle.update()

    def run(self, steps: int):
           self.logger = DataLogger(self.vehicles)
           try: 
                self.logger.open_log()
                self.logger.log_state(tick=0)
                        
           
                for tick in range(1, steps+1):
                    self.step()
                    self.logger.log_state(tick=self.time)
           finally:
                self.logger.close_log()

                    

