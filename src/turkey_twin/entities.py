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
    target_location: Location = None

    def set_destination(self, dest_x: float, dest_y: float):
        
        self.target_location = Location(x=dest_x, y=dest_y)

    def update(self):

        if self.target_location is not None:
            dx = self.target_location.x - self.location.x
            dy = self.target_location.y - self.location.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance < self.speed:
                battery_cost = distance * .5
                if self.battery_level > battery_cost:
                    self.location.x = self.target_location.x
                    self.location.y = self.target_location.y
                    self.battery_level -= battery_cost
                    self.target_location = None
                    self.status = "IDLE"
                    print(f" -> Vehicle {self.id} reached destination {self.location}. Battery: {self.battery_level}")
                else:
                    print(f"!!!!! Vehicle {self.id} cannot reach destination, not enough battery!")
                    self.status = "DEAD_BATTERY"

            #increment movement toward target
            else:
                battery_step_cost = self.speed * .5

                if self.battery_level >= battery_step_cost:
                    
                    direction_x = dx/distance
                    direction_y = dy/distance

                    self.location.x += direction_x * self.speed
                    self.location.y += direction_y * self.speed

                    self.status = "MOVING"
                    self.battery_level -= battery_step_cost


                else:
                    print(f"!!!!! Vehicle {self.id} is out of battery during movement!")
                    self.status = "DEAD_BATTERY"

    #this is not really needed at the moment
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
            
