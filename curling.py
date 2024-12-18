"""
Curling portion of the ECEG341 Robot Olympics
11/18/2024
Mike Merola and Miguel Romero
"""

import asyncio
from machine import Pin
from array import array
from bot import Bot
import neopixel
from lineFollow import line_follow

async def curling_logic(bot, n, task2):
    """
    Implements the logic for the robot to stop at a specific distance from the wall during
    the Curling portion of the competition.

    Parameters:
        bot (Bot): An instance of the Bot class to control the robot.
        n (NeoPixel): NeoPixel LED object used for visual feedback.
        task2 (asyncio.Task): The `line_follow` task, which will be canceled when the robot
                              reaches the target distance.
                              """

    while True:
        distance = bot.read_distance()
        distance_to_wall = 45
        if distance is None:
            bot.brakes()
            continue
        if  (distance <= distance_to_wall):
            bot.stop()
            for i in range(2):
                n[i] = (0, 255, 0)
                n.write()
            task2.cancel()
        else:
            n[0] = (255, 0, 0)  # Set the first LED to red
            n[1] = (255, 0, 0)  # Set the second LED to red
            n.write()
        await asyncio.sleep(0.01)

async def curling():
    """
    Initializes and runs the robot for the Curling portion of the ECEG341 Robot Olympics.
     """
    conf ={
        "trig_pin" : 16,
        "echo_pin" : 17,
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
    n = neopixel.NeoPixel(Pin(18),32)
    ind = Pin(0, Pin.OUT)
    task2 = asyncio.create_task(line_follow(bot, ind , state, count ,start_time, n, speed_container= 0.9))
    task1 = asyncio.create_task(curling_logic(bot, n, task2))
    await asyncio.gather(task1,task2)



asyncio.run(curling())
