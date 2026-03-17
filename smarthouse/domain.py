import random
from datetime import datetime

class Measurement:
    """
    This class represents a measurement taken from a sensor.
    """

    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit



# TODO: Add your own classes here!
class Floor:
    def __init__(self, level):
        self.level = level
        self.rooms = []
    
    def get_area(self):
        total_area = 0
        for room in self.rooms:
            total_area += room.size
        return total_area
    
class Room:
    def __init__(self, floor, size, name=None):
        self.floor = floor
        self.size = size
        self.room_name = name
        self.devices = []

class Device:
    def __init__(self, id, device_type, supplier, model_name):
        self.id = id
        self.device_type = device_type
        self.supplier = supplier
        self.model_name = model_name
        self.room = None
    
    def is_sensor(self):
        return False

    def is_actuator(self):
        return False
    
    def get_device_type(self):
        return self.device_type
    
class Sensor(Device):
    def __init__(self, id, device_type, supplier, model_name):
        super().__init__(id, device_type, supplier, model_name)
        self.measurements = []

    def is_sensor(self):
        return True
    
    def get_measurements(self):
        return self.measurements
    
    def last_measurements(self): #TODO
        if self.measurements:
            return self.measurements[-1]
        return None
    
    def last_measurement(self):
        return Measurement(
            datetime.now().isoformat(),
            random.uniform(10, 30),
            "°C"
        )

class Actuator(Device):
    def __init__(self, id, device_type, supplier, model_name):
        super().__init__(id, device_type, supplier, model_name)
        self.is_on = False
        self.value = None
    
    def is_actuator(self):
        return True
    
    def turn_on(self, value=None):
        self.is_on = True
        self.value = value
    
    def turn_off(self):
        self.is_on = False
        self.value = None

    def is_active(self):
        return self.is_on

class SmartHouse:
    """
    This class serves as the main entity and entry point for the SmartHouse system app.
    Do not delete this class nor its predefined methods since other parts of the
    application may depend on it (you are free to add as many new methods as you like, though).

    The SmartHouse class provides functionality to register rooms and floors (i.e. changing the 
    house's physical layout) as well as register and modify smart devices and their state.
    """
    def __init__(self):
        self.floors = []
        self.devices = []


    
    def register_floor(self, level):
        """
        This method registers a new floor at the given level in the house
        and returns the respective floor object.
        """
        floor = Floor(level)
        self.floors.append(floor)
        
        def get_level(f):
            return f.level
        
        self.floors.sort(key=get_level)

        return floor




    def register_room(self, floor, room_size, room_name = None):
        """
        This methods registers a new room with the given room areal size 
        at the given floor. Optionally the room may be assigned a mnemonic name.
        """
        room = Room(floor, room_size, room_name)
        floor.rooms.append(room)
        return room


    def get_floors(self):
        """
        This method returns the list of registered floors in the house.
        The list is ordered by the floor levels, e.g. if the house has 
        registered a basement (level=0), a ground floor (level=1) and a first floor 
        (leve=1), then the resulting list contains these three flors in the above order.
        """
        return self.floors


    def get_rooms(self):
        """
        This methods returns the list of all registered rooms in the house.
        The resulting list has no particular order.
        """
        rooms = []
        for floor in self.floors:
            rooms.extend(floor.rooms)
        return rooms

    def get_area(self):
        """
        This methods return the total area size of the house, i.e. the sum of the area sizes of each room in the house.
        """
        total_area = 0
        for room in self.get_rooms():
            total_area+=room.size
        return total_area

    def register_device(self, room, device):
        """
        This methods registers a given device in a given room.
        """
        if device.room:
            device.room.devices.remove(device)

        room.devices.append(device)
        device.room = room

        if device not in self.devices:
            self.devices.append(device)

    def get_devices(self):
        return self.devices
    
    def get_device_by_id(self, device_id):
        """
        This method retrieves a device object via its id.
        """
        for device in self.devices:
            if device.id == device_id:
                return device
        return None
                

