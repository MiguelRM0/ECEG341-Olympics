import asyncio
from machine import Pin
from array import array
from main import Bot
import neopixel
from lineFollow import line_follow

async def curling(bot, n):
    while True:
        distance = bot.read_distance()
        distance_to_wall = 45
        if distance is None:
            bot.brakes()
            continue
        if  (distance <= distance_to_wall):
            bot.brakes()
            for i in range(2):
                n[i] = (0, 255, 0)
                n.write()
        else:
            n[0] = (255, 0, 0)  # Set the first LED to red
            n[1] = (255, 0, 0)  # Set the second LED to red
            n.write()
            bot.fwd()

async def main():
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
    n = neopixel.NeoPixel(machine.Pin(18),32)
    task1 = asyncio.create_task(curling(bot, n))
    task2 = asyncio.create_task(asyncio.to_thread(line_follow, state, count, start_time, n))
    await asyncio.gather(task1,task2)
