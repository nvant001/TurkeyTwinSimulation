from dataclasses import dataclass
from typing import List
import math


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

    def move_to(self, new_x: float, new_y: float):

        distance = math.sqrt((new_x - self.location.x)**2 + (new_y - self.location.y)**2)
        energy_cost = distance/2

        if self.battery_level >= energy_cost:
            self.location.x = new_x
            self.location.y = new_y
            self.battery_level -= energy_cost
            self.status = "MOVING"
            print(f" -> Vehicle {self.id} moved to {self.location}. Battery: {self.battery_level}")
        else:
            self.status = "DEAD_BATTERY"
            print(f"!!!!! Vehcile {self.id} is stuck! Not enough batter to move {distance:.2f%}, Battery level is only {self.battery_level:.1f%} when {energy_cost:.1f%} is needed!")
            
