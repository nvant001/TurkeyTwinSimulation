# src/turkey_twin/models.py
from pydantic import BaseModel
from typing import List, Optional

class VehicleStatus(BaseModel):
    #Data structure for a single vehicle status report

    id: str
    x: float
    y: float
    battery_level: float
    status: str

class APIResponse(BaseModel):

    message: str
    tick: Optional[int] = None