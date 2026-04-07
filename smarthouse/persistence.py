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
        cursor.execute("""SELECT id, floor, area, name 
                        FROM rooms""")
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

        #load actuator states
        cursor.execute("""SELECT device_id, is_on, value FROM actuator_states""")
        actuator_states = {}
        for row in cursor.fetchall():
            device_id = row[0]
            is_on = row[1]
            value = row[2]
            actuator_states[device_id] = (is_on, value)

        # gets devices
        cursor.execute("""SELECT id, room, kind, category, supplier, product 
                        FROM devices""")
        devices_data = cursor.fetchall()

        #goes through all the devices from db
        for dev_id, room_id, kind, category, supplier, product in devices_data:
            
            #device and actuator
            if category.strip().lower() == "sensor":
                device = Sensor(dev_id, category, supplier, product)
            else:
                device = Actuator(dev_id, category, supplier, product)

                if dev_id in actuator_states:
                    is_on, value = actuator_states[dev_id]
                    device.is_on = bool(is_on)
                    device.value = value

            # find device room
            if room_id in rooms:
                smarthouse.register_device(rooms[room_id], device)

        cursor.close()
        return smarthouse


    def get_latest_reading(self, sensor) -> Optional[Measurement]:
        """
        Retrieves the most recent sensor reading for the given sensor if available.
        Returns None if the given object has no sensor readings.
        """
        if not sensor or not sensor.id:
            return None
        
        cursor = self.cursor()
        
        # gets last measurement from sensor
        cursor.execute("""SELECT ts, value, unit 
                          FROM measurements 
                          WHERE device = ? 
                          ORDER BY ts DESC 
                          LIMIT 1""", (sensor.id,))
        
        result = cursor.fetchone()
        cursor.close()

        if result != None:
            timestamp = result[0]
            value = result[1]
            unit = result[2]
            return Measurement(timestamp, value, unit)
        
        return None


    def update_actuator_state(self, actuator):
        """
        Saves the state of the given actuator in the database. 
        """
      
        cursor = self.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS actuator_states (
                        device_id TEXT PRIMARY KEY,
                        is_on INTEGER,
                        value REAL)""")

        cursor.execute("""INSERT INTO actuator_states (device_id, is_on, value) 
                          VALUES (?, ?, ?)
                          ON CONFLICT(device_id) DO UPDATE SET is_on = excluded.is_on, value = excluded.value""", 
                          (actuator.id, actuator.is_active(), actuator.value))
        
        self.conn.commit()
        cursor.close()


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
        cursor = self.cursor()

        device_ids = []
        for device in room.devices:
            device_ids.append(device.id)

        if not device_ids:
            return {}

        query = """SELECT DATE(ts), AVG(value)
                    FROM measurements
                    WHERE device IN ({})
                    AND unit = '°C'""".format(",".join(["?"] * len(device_ids)))

        params = list(device_ids)

        if from_date:
            query += " AND ts >= ?"
            params.append(from_date)

        if until_date:
            query += " AND ts <= ?"
            params.append(until_date)

        query += " GROUP BY DATE(ts)"

        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()

        avg_temps = {}
        for date, avg in results:
            avg_temps[date] = avg

        return avg_temps

    
    def calc_hours_with_humidity_above(self, room, date: str) -> list:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of number representing hours [0-23].
        """
        # TODO: implement
        return NotImplemented

#---------------------------------------------------------------------------
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
    print("\n--- Testing get_latest_reading() ---")

    house = repo.load_smarthouse_deep()

    sensor = None
    for device in house.get_devices():
        if device.is_sensor():
            sensor = device
            break

    if sensor:
        reading = repo.get_latest_reading(sensor)

        print("Sensor ID:", sensor.id)
        if reading:
            print("Timestamp:", reading.timestamp)
            print("Value:", reading.value)
            print("Unit:", reading.unit)
        else:
            print("No reading found")
    else:
        print("No sensor found")

    
    print("\n--- Testing update_actuator_state() ---")

    actuator = None
    for device in house.get_devices():
        if device.is_actuator():
            actuator = device
            break

    if actuator:
        print("Actuator ID:", actuator.id)

        actuator.turn_on(22.5)
        repo.update_actuator_state(actuator)
        print("Turned ON with value:", actuator.value)

        actuator.turn_off()
        repo.update_actuator_state(actuator)
        print("Turned OFF")

        cursor = repo.cursor()
        cursor.execute("SELECT * FROM actuator_states WHERE device_id = ?", (actuator.id,))
        result = cursor.fetchone()
        cursor.close()

        print("Stored in DB:", result)
    else:
        print("No actuator found")

    print("\n--- Testing avg temp ---")

    room = house.get_rooms()[0]
    result = repo.calc_avg_temperatures_in_room(room)

    print(result)