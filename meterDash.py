"""
Meter Dash  portion of the ECEG341 Robot Olympics
11/18/2024
Mike Merola and Miguel Romero
"""
import asyncio
from bot import Bot
from machine import Pin
import neopixel
from lineFollow import line_follow

async def dash(bot, speed_container):
    """
    Continuously monitors the distance to obstacles using the bot's ultrasonic sensor
    and adjusts the bot's speed accordingly.

    Parameters:
        bot (Bot): An instance of the Bot class to control the robot.
        speed_container (list): A mutable list containing the current speed of the robot.
                                The speed is adjusted based on the distance readings.
    """

    while True:
        distance = bot.read_distance()
        # print(distance)
        if distance is None:
            bot.stop()
            speed_container[0] = 0
            continue
        if distance < 10:
            # bot.stop()
            speed_container[0] = 0
        elif distance >= 10:
            speed_container[0] = 0.7
        await asyncio.sleep(0.01)

async def meterDash():
    """
    Initializes the robot's configuration, sets up tasks for line-following and
    obstacle detection, and manages the robot's participation in the Meter Dash challenge.

     Behavior:
        - Configures the bot's hardware, including motor control pins, sensors, and LEDs.
        - Creates and runs two asynchronous tasks:
            1. `line_follow`: Handles the line-following behavior of the robot.
            2. `dash`: Monitors the distance to obstacles and adjusts the speed.
        - Ensures both tasks run concurrently using `asyncio.gather`.
     """
    conf = {
        "trig_pin": 16,
        "echo_pin": 17,
        "M1A": 8,
        "M1B": 9,
        "M2A": 11,
        "M2B": 10,
        "left_sensor": 27,
        "right_sensor": 26,
        "A": 20,
        "B": 21
    }
    bot = Bot(**conf)

    state = 0
    count = 0
    start_time = None
    ind = Pin(0, Pin.OUT)
    n = neopixel.NeoPixel(Pin(18), 32)

    speed_container = [0.7]  # Initial speed

    task2 = asyncio.create_task(line_follow(bot, ind, state, count, start_time, n, speed_container))
    task1 = asyncio.create_task(dash(bot, speed_container))

    await asyncio.gather(task1, task2)

asyncio.run(meterDash())
