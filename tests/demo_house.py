from smarthouse.domain import SmartHouse, Sensor, Actuator

DEMO_HOUSE = SmartHouse()

# Building house structure
ground_floor = DEMO_HOUSE.register_floor(1)
second_floor = DEMO_HOUSE.register_floor(2)

entrance = DEMO_HOUSE.register_room(ground_floor, 13.5, "Entrance")
living = DEMO_HOUSE.register_room(ground_floor, 39.75, "LivingRoom/Kitchen")
bath1 = DEMO_HOUSE.register_room(ground_floor, 6.3, "Bathroom 1")
guest1 = DEMO_HOUSE.register_room(ground_floor, 8, "Guest Room 1")
garage = DEMO_HOUSE.register_room(ground_floor, 19, "Garage")

master = DEMO_HOUSE.register_room(second_floor, 17, "Master Bedroom")
guest3 = DEMO_HOUSE.register_room(second_floor, 10, "Guest Room 3")
office = DEMO_HOUSE.register_room(second_floor, 11.75, "Office")
bath2 = DEMO_HOUSE.register_room(second_floor, 9.25, "Bathroom 2")
guest2 = DEMO_HOUSE.register_room(second_floor, 8, "Guest Room 2")
hallway = DEMO_HOUSE.register_room(second_floor, 10, "Hallway")
dresser = DEMO_HOUSE.register_room(second_floor, 4, "Dressing Room")
# TODO: continue registering the remaining floor, rooms and devices

# Etasje 1
d1 = Actuator("4d5f1ac6-906a-4fd1-b4bf-3a0671e4c4f1", "Smart Lock", "MythicalTech", "Guardian Lock 7000")
d2 = Sensor("8a43b2d7-e8d3-4f3d-b832-7dbf37bf629e", "CO2 sensor", "ElysianTech", "Smoke Warden 1000")
d3 = Sensor("a2f8690f-2b3a-43cd-90b8-9deea98b42a7", "Electricity Meter", "MysticEnergy Innovations", "Volt Watch Elite")
d4 = Actuator("5e13cabc-5c58-4bb3-82a2-3039e4480a6d", "Heat Pump", "ElysianTech", "Thermo Smart 6000")
d5 = Sensor("cd5be4e8-0e6b-4cb5-a21f-819d06cf5fc5", "Motion Sensor", "NebulaGuard Innovations", "MoveZ Detect 69")
d6 = Sensor("3d87e5c0-8716-4b0b-9c67-087eaaed7b45", "Humidity Sensor", "AetherCorp", "Aqua Alert 800")
d7 = Actuator("8d4e4c98-21a9-4d1e-bf18-523285ad90f6", "Smart Oven", "AetherCorp", "Pheonix HEAT 333")
d8 = Actuator("9a54c1ec-0cb5-45a7-b20d-2a7349f1b132", "Automatic Garage Door", "MythicalTech", "Guardian Lock 9000")

# Etasje 2
d9 = Actuator("c1e8fa9c-4b8d-487a-a1a5-2b148ee9d2d1", "Smart Oven", "IgnisTech Solutions", "Ember Heat 3000")
d10 = Sensor("4d8b1d62-7921-4917-9b70-bbd31f6e2e8e", "Temperature Sensor", "AetherCorp", "SmartTemp 42")
d11 = Sensor("7c6e35e1-2d8b-4d81-a586-5d01a03bb02c", "Air Quality Sensor", "CelestialSense Technologies", "AeroGuard Pro")
d12 = Actuator("1a66c3d6-22b2-446e-bf5c-eb5b9d1a8c79", "Smart Plug", "MysticEnergy Innovations", "FlowState X")
d13 = Actuator("9e5b8274-4e77-4e4e-80d2-b40d648ea02a", "Dehumidifier", "ArcaneTech Solutions", "Hydra Dry 8000")
d14 = Actuator("6b1c5f6b-37f6-4e3d-9145-1cfbe2f1fc28", "Light Bulp", "Elysian Tech", "Lumina Glow 4000")

# Etasje 1
DEMO_HOUSE.register_device(entrance, d1)
DEMO_HOUSE.register_device(living, d2)
DEMO_HOUSE.register_device(entrance, d3)
DEMO_HOUSE.register_device(living, d4)
DEMO_HOUSE.register_device(living, d5)
DEMO_HOUSE.register_device(bath1, d6)
DEMO_HOUSE.register_device(guest1, d7)
DEMO_HOUSE.register_device(garage, d8)

# Etasje 2
DEMO_HOUSE.register_device(master, d9)
DEMO_HOUSE.register_device(master, d10)
DEMO_HOUSE.register_device(guest3, d11)
DEMO_HOUSE.register_device(office, d12)
DEMO_HOUSE.register_device(bath2, d13)
DEMO_HOUSE.register_device(guest2, d14)