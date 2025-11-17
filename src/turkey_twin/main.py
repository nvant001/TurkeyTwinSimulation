# src/turkey_twin/main.py
import sys
import datetime
from entities import Vehicle, Warehouse, Location
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
    print(f"     Moving {truck_1} to (3,4)")
    truck_1.move_to(3, 4)
    print(f"     Moving {truck_1} to (10,10)")
    truck_1.move_to(10, 10)

    print(f"\nFinal State: {truck_1}")



if __name__ == "__main__":
    start_simulation()