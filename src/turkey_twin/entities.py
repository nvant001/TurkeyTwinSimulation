# src/turkey_twin/entities.py
from dataclasses import dataclass, field
from typing import List
import math
from turkey_twin.map_graph import MapGraph

@dataclass
class Location:
    #Our coordinates on a 2d grid

    x: float
    y: float

    def __repr__(self):
        return f"({self.x:.2f}, {self.y:.2f})"
    

@dataclass
class Warehouse:
    #static warehouse that has inventory
    id: str
    location: Location
    inventory_count: int = 100 #A default starting inventory value that we can change

@dataclass
class Vehicle:
    #Delivery Truck

    id: str
    location: Location
    battery_level: float = 100.0 #starts full
    speed: float = 1.0 #default speed
    status: str = "IDLE" #default status of vehicle
    target_location: Location = None
    path_route: List[Location] = field(default_factory=list)
    map_ref: MapGraph =  field(default=None, repr=False)

    def set_destination(self, dest_x: float, dest_y: float):
        if not self.map_ref:
            print("[ERROR]: Vehicle has no MapGraph reference.")
            return

        # 1. Convert float current/dest to integer grid coordinates
        start_grid = (int(self.location.x), int(self.location.y))
        end_grid = (int(dest_x), int(dest_y))
        
        # 2. Find the path
        grid_path = self.map_ref.find_path(start_grid, end_grid)
        
        if not grid_path:
            self.status = "BLOCKED"
            print(f"!! Vehicle {self.id} cannot find path to {end_grid}.")
            return
            
        # 3. Convert path back to Location objects and store (excluding current position)
        self.path_route = [Location(float(x), float(y)) for x, y in grid_path[1:]] 
        self.target_location = self.path_route[0] if self.path_route else None
        self.status = "PATHING"
        print(f"Vehicle {self.id} set route with {len(self.path_route)} steps.")

    def update(self):
            """
            Called every tick to advance the vehicle's position along its path.
            """
            
            # 1. Grab the next sub-target if the current one was reached (or is empty)
            if self.target_location is None and self.path_route:
                self.target_location = self.path_route.pop(0)
                self.status = "MOVING" 
            
            # 2. Execute movement toward the target
            if self.target_location is not None:
                dx = self.target_location.x - self.location.x
                dy = self.target_location.y - self.location.y
                distance = math.sqrt(dx**2 + dy**2)


                if distance <= self.speed:
                    battery_cost = distance * 0.5 
                    
                    if self.battery_level > battery_cost:
              
                        self.location.x = self.target_location.x
                        self.location.y = self.target_location.y
                        self.battery_level -= battery_cost
                        
                        self.target_location = None 
                        
                    
                        if not self.path_route:
                            self.status = "IDLE"
                            print(f" -> Vehicle {self.id} ARRIVED at final destination {self.location}. Battery: {self.battery_level:.2f}")
              
                        
                    else:
                        self.status = "DEAD_BATTERY"
                        print(f"!!!!! Vehicle {self.id} cannot reach destination, not enough battery!")

               
                else:
                    battery_step_cost = self.speed * 0.5

                    if self.battery_level >= battery_step_cost:
                        
                        direction_x = dx/distance
                        direction_y = dy/distance

                        self.location.x += direction_x * self.speed
                        self.location.y += direction_y * self.speed

                        self.status = "MOVING"
                        self.battery_level -= battery_step_cost
                        
                    else:
                        self.status = "DEAD_BATTERY"
                        print(f"!!!!! Vehicle {self.id} is out of battery during movement!")

    