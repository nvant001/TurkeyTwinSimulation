# src/turkey_twin/api.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import List

from turkey_twin.engine import SimulationEngine
from turkey_twin.entities import Vehicle, Location
from turkey_twin.map_graph import MapGraph
from turkey_twin.models import VehicleStatus, APIResponse

# Global instances
map_graph = MapGraph(size=10)
engine = SimulationEngine()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP LOGIC ---
    print("Initializing Simulation Engine & Database...")
    
    # Setup Logic
    test_truck = Vehicle(id="API-Tk-01", location=Location(x=0, y=0), map_ref=map_graph)
    engine.add_vehicle(test_truck)
    test_truck.set_destination(9, 9)
    
    # Initialize DB Connection
    engine.initialize_logger()
    
    yield
    
    # --- SHUTDOWN LOGIC ---
    print("Closing Database Connection...")
    if engine.logger:
        engine.logger.close_log()

app = FastAPI(title="Turkey Twin API", lifespan=lifespan)

@app.get("/", response_model=APIResponse)
def root():
    return {"message": "Turkey Twin API is running."}

@app.get("/status/fleet", response_model=List[VehicleStatus])
def get_fleet_status():
    fleet_status = []
    for vehicle in engine.vehicles: # Fixed typo 'vehcile'
        fleet_status.append(VehicleStatus(
            id=vehicle.id, 
            x=vehicle.location.x,
            y=vehicle.location.y,
            battery_level=vehicle.battery_level,
            status=vehicle.status
        ))
    return fleet_status

@app.post("/control/step/{num_steps}", response_model=APIResponse)
def control_steps(num_steps: int = 1):
    if num_steps <= 0:
        return APIResponse(message="Steps must be positive.", tick=engine.time)
    
    for _ in range(num_steps):
        # THIS was the missing link: tell engine to log to DB
        engine.step(log_to_db=True)

    return APIResponse(message=f"Advanced simulation by {num_steps} steps.", tick=engine.time)

@app.post("/control/reset", response_model=APIResponse)
def reset_simulation():
    """Resets the DB and moves truck back to start."""
    if engine.logger:
        engine.logger.clear_log()
    
    # Reset vehicle physics
    for v in engine.vehicles:
        v.location.x = 0
        v.location.y = 0
        v.battery_level = 100.0
        v.path_route = []
        v.target_location = None
        v.set_destination(9, 9) # Send it back on its way
        
    engine.time = 0
    # Log the initial 0 state
    if engine.logger:
        engine.logger.log_state(0)
        
    return APIResponse(message="Simulation Reset.", tick=0)