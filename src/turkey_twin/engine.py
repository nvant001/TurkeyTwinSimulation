from entities import Vehicle, Warehouse, Location
import datetime

class SimulationEngine:
    time = 0
    vehicles: list[Vehicle] = []
    warehouses: list[Warehouse] = []

    def add_vehicle(self, vehicle: Vehicle):
        self.vehicles.append(vehicle)
        print(f"[{datetime.datetime.now()}]: Vehicle {vehicle.id} added to simulation.")

    def step(self):
        self.time += 1
        print(f"[{datetime.datetime.now()}]: Simulation time step {self.time}")
        for vehicle in self.vehicles:
            vehicle.update()

    def run(self, steps: int):
        for _ in range(steps):
            self.step()