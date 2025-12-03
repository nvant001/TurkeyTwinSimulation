from fastapi import FastAPI
from engine import SimulationEngine
from entities import Vehicle, Warehouse, Location
from map_graph import MapGraph
from models import VehicleStatus, APIResponse
from typing import List
import uvicorn

map_graph = MapGraph(size=10)
engine = SimulationEngine()

test_truck = Vehicle(id="API-Tk-01", location=Location(x=0, y=0), map_ref=map_graph)
engine.add_vehicle(test_truck)
test_truck.set_destination(9, 9)

app = FastAPI(title="Turkey Twin API")

@app.get("/", response_model=APIResponse)
def root():
    return {"message": "Turkey Twin API is running."}


@app.get("/status/fleet", response_model=List[VehicleStatus])
def get_fleet_status():
    fleet_status = []
    for vehcile in engine.vehicles:
        fleet_status.append(VehicleStatus(
            id=vehcile.id, 
            x=vehcile.location.x,
            y=vehcile.location.y,
            battery_level=vehcile.battery_level,
            status=vehcile.status
        ))
    return fleet_status

@app.post("/control/step/{num_steps}", response_model=APIResponse)
def control_steps(num_steps: int = 1):
    if num_steps <= 0:
        return APIResponse(message="Number of steps must be positive.", tick=engine.time)
    
    for _ in range(num_steps):
        engine.step()

    return APIResponse(message=f"Advanced simulation by {num_steps} steps.", tick=engine.time)