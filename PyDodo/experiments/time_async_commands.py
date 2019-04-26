from pydodo import (change_altitude, change_heading, change_speed,
                    aircraft_position, all_positions,
                    reset_simulation, create_aircraft,
                    async_change_altitude, batch)
import time

reset_simulation()

aircraft_id = "TST1001"
type = "B744"
latitude = 0
longitude = 0
heading = 0
flight_level = 250
speed = 200

cmd = create_aircraft(aircraft_id = aircraft_id,
                      type = type,
                      latitude = latitude,
                      longitude = longitude,
                      heading = heading,
                      flight_level = flight_level,
                      speed = speed)


t = time.time()
print('Waiting...')
while True:
    pos = all_positions()
    # print(format_runtime(time.time()-start))

    if time.time()-t > 3:
        print("Sending synchronous commands...")
        t = time.time()
        for i in range(300, 400, 10):
            change_altitude(aircraft_id = aircraft_id, flight_level = i)
        print('Time to run 10 synchronous commands: {}'.format(time.time()-t))

        print("Sending asynchronous commands...")
        t = time.time()
        commands = []
        for i in range(400, 300, -10):
            commands.append(async_change_altitude(aircraft_id = aircraft_id, flight_level = i))
        response = batch(commands)
        # print(response)
        print('Time to run 10 asynchronous commands: {}'.format(time.time()-t))

        break


print('DONE')
