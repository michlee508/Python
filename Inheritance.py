""" Inheritance - vehicle example """

class Vehicle:
    def __init__(self):
        self._headlight_status = False

    @property
    def headlight_status(self):  # getter
        return self._headlight_status

    @headlight_status.setter
    def headlight_status(self, state: bool):  # setter
        self._headlight_status = state


class GasVehicle(Vehicle):  # param to access attributes from parent class
    def __init__(self):
        self._tank_status = "Empty"
        super().__init__()  # super() returns headlight attribute from parent class Vehicle.

    def fuel_up(self):
        print("Going to the gas station")


class ElectricVehicle(Vehicle):  # param to access attributes from parent class
    def __init__(self):
        self._battery_status = "Empty"
        super().__init__()  # super() returns headlight attribute from parent class Vehicle.

    def fuel_up(self):
        print("Charging now!")
        self._battery_status = "Full"

rusty = ElectricVehicle()  # chg from GasVehicle() to ElectricVehicle() back and forth to test
if rusty.headlight_status:
    print("Headlights on!")
else:
    print("headlights off")
# rusty.headlight_status = False
rusty.fuel_up()

r"""
--- sample outout ---
headlights off
Charging now!
"""

