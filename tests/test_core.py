import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.turkey_twin.entities import Vehicle, Location


@pytest.fixture
def new_vehicle():
    return Vehicle(id='Test',location=Location(x=0,y=0))

def test_vehicle_initializations(new_vehicle):
    assert new_vehicle.status == "IDLE"

def test_movement(new_vehicle):
    new_vehicle.set_destination(10.0, 10.0)
    new_vehicle.update()
    assert new_vehicle.battery_level == pytest.approx(100.0 - new_vehicle.speed * .5)

def test_snapping_status(new_vehicle):
    new_vehicle.set_destination(.2, .2)
    new_vehicle.update()
    assert new_vehicle.

