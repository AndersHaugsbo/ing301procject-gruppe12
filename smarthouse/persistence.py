import sqlite3
from pathlib import Path
from typing import Optional
from smarthouse.domain import Measurement, SmartHouse, Sensor, Actuator

class SmartHouseRepository:
    """
    Provides the functionality to persist and load a _SmartHouse_ object 
    in a SQLite database.
    """

    def __init__(self, file: str) -> None:
        self.file = file 
        self.conn = sqlite3.connect(file, check_same_thread=False)

    def __del__(self):
        self.conn.close()

    def cursor(self) -> sqlite3.Cursor:
        """
        Provides a _raw_ SQLite cursor to interact with the database.
        When calling this method to obtain a cursors, you have to 
        rememeber calling `commit/rollback` and `close` yourself when
        you are done with issuing SQL commands.
        """
        return self.conn.cursor()

    def reconnect(self):
        self.conn.close()
        self.conn = sqlite3.connect(self.file)

    #---------------------------------------------------------------------------------
    
    def load_smarthouse_deep(self):
        """
        This method retrives the complete single instance of the _SmartHouse_ 
        object stored in this database. The retrieval yields a _deep_ copy, i.e.
        all referenced objects within the object structure (e.g. floors, rooms, devices) 
        are retrieved as well. 
        """
        smarthouse = SmartHouse()
        cursor = self.cursor()

        # gets rooms
        cursor.execute("SELECT id, floor, area, name FROM rooms")
        rooms_data = cursor.fetchall()

        floors = {}
        rooms = {}

        #goes through all the rooms from db
        for room_id, floor_level, area, name in rooms_data:
            #creates floor
            if floor_level not in floors:
                floors[floor_level] = smarthouse.register_floor(floor_level)

            floor_obj = floors[floor_level]

            #creates room and add to floor
            room_obj = smarthouse.register_room(floor_obj, area, name)
            rooms[room_id] = room_obj

        # gets devices
        cursor.execute("SELECT id, room, kind, category, supplier, product FROM devices")
        devices_data = cursor.fetchall()

        #goes through all the devices from db
        for dev_id, room_id, kind, category, supplier, product in devices_data:

            #device og acutator
            if kind.lower() == "sensor":
                device = Sensor(dev_id, category, supplier, product)
            else:
                device = Actuator(dev_id, category, supplier, product)

            # find devise room
            if room_id in rooms:
                smarthouse.register_device(rooms[room_id], device)

        cursor.close()
        return smarthouse


    def get_latest_reading(self, sensor) -> Optional[Measurement]:
        """
        Retrieves the most recent sensor reading for the given sensor if available.
        Returns None if the given object has no sensor readings.
        """
        # TODO: After loading the smarthouse, continue here
        return NotImplemented


    def update_actuator_state(self, actuator):
        """
        Saves the state of the given actuator in the database. 
        """
        # TODO: Implement this method. You will probably need to extend the existing database structure: e.g.
        #       by creating a new table (`CREATE`), adding some data to it (`INSERT`) first, and then issue
        #       and SQL `UPDATE` statement. Remember also that you will have to call `commit()` on the `Connection`
        #       stored in the `self.conn` instance variable.
        pass


    # statistics

    
    def calc_avg_temperatures_in_room(self, room, from_date: Optional[str] = None, until_date: Optional[str] = None) -> dict:
        """Calculates the average temperatures in the given room for the given time range by
        fetching all available temperature sensor data (either from a dedicated temperature sensor 
        or from an actuator, which includes a temperature sensor like a heat pump) from the devices 
        located in that room, filtering the measurement by given time range.
        The latter is provided by two strings, each containing a date in the ISO 8601 format.
        If one argument is empty, it means that the upper and/or lower bound of the time range are unbounded.
        The result should be a dictionary where the keys are strings representing dates (iso format) and 
        the values are floating point numbers containing the average temperature that day.
        """
        # TODO: This and the following statistic method are a bit more challenging. Try to design the respective 
        #       SQL statements first in a SQL editor like Dbeaver and then copy it over here.  
        return NotImplemented

    
    def calc_hours_with_humidity_above(self, room, date: str) -> list:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of number representing hours [0-23].
        """
        # TODO: implement
        return NotImplemented


if __name__ == "__main__":
    
    repo = SmartHouseRepository("../data/db.sql")

    house = repo.load_smarthouse_deep()

    print("Antall rom:", len(house.get_rooms()))

    print("Totalt areal:", house.get_area())

    print("Antall devices:", len(house.get_devices()))

    device = house.get_devices()[0]
    print("Eksempel device:")
    print("  ID:", device.id)
    print("  Type:", device.get_device_type())
    print("  Rom:", device.room.room_name if device.room else None)
