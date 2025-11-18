# src/turkey_twin/main.py
import sys
import datetime
from entities import Vehicle, Warehouse, Location
from engine import SimulationEngine
def start_simulation():
    print(f"[{datetime.datetime.now()}]: Simulation started")
    print(f"python version: {sys.version.split()[0]}")
    print("System is ready")

    print("\n[1] Initializing World...")
    main_hub = Warehouse(id="WH-001", location=Location(x=0, y=0))
    print(f"        Created main hub: {main_hub}")

    print("\n[2] Deploying Fleet...")
    truck_1 = Vehicle(id="Tk-01", location=Location(x=0, y=0))
    print(f"        Deployed {truck_1}")

    print("\n[3]Testing Physics...")
    engine = SimulationEngine()
    engine.add_vehicle(truck_1)
    truck_1.set_destination(10, 40)
    engine.run(steps=35)


    print(f"\nFinal State: {truck_1}")



if __name__ == "__main__":
    start_simulation()