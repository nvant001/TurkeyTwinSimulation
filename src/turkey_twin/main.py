import sys
import datetime

def start_simulation():
    print(f"[{datetime.datetime.now()}]: Simulation started")
    print(f"python version: {sys.version.split()[0]}")
    print("System is ready")

if __name__ == "__main__":
    start_simulation()