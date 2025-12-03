# src/turkey_twin/main.py
import sys
import datetime
from turkey_twin.entities import Vehicle, Warehouse, Location
from turkey_twin.engine import SimulationEngine
from turkey_twin.map_graph import MapGraph
def start_simulation():
    print(f"[{datetime.datetime.now()}]: Simulation started")
    print(f"python version: {sys.version.split()[0]}")
    print("System is ready")

    print("\n[1] Initializing World...")
    world_map = MapGraph(size=10)
    main_hub = Warehouse(id="WH-001", location=Location(x=0, y=0))
    dest_hub = Warehouse(id="WH-002", location=Location(x=9, y=9))

    print("\n[2] Deploying Fleet...")
    truck_1 = Vehicle(id="Tk-01", location=Location(x=0, y=0), map_ref=world_map)
    print(f"        Deployed {truck_1}")
    truck_2 = Vehicle(id="Tk-02", location=Location(x=5, y=5), map_ref=world_map)
    print(f"        Deployed {truck_2}")

    print("\n[3]Testing Physics...")
    engine = SimulationEngine()
    engine.add_vehicle(truck_1)
    engine.add_vehicle(truck_2)
    truck_1.set_destination(dest_hub.location.x, dest_hub.location.y)
    truck_2.set_destination(dest_hub.location.x, dest_hub.location.y)
    engine.run_batch(steps=100)


    print(f"\nFinal State: {truck_1}") 
    print(f"\nFinal State: {truck_2}")



if __name__ == "__main__":
    start_simulation()