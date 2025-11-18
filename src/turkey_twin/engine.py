from entities import Vehicle, Warehouse, Location
import datetime
import csv

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
        filename = f"data/simulation_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile) 
            header = ['tick' , 'vehicle_id' ,'x','y','battery','status']
            writer.writerow(header)
            for tick in range(steps):
                self.step()
                for vehicle in self.vehicles:
                    line = [tick, vehicle.id, vehicle.location.x, vehicle.location.y, vehicle.battery_level, vehicle.status]
                    writer.writerow(line)

