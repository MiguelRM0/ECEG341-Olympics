from bot import Bot
from machine import Pin
import neopixel
from lineFollow import line_follow
import asyncio

async def marathon():
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
    ind = Pin(0, Pin.OUT)
    n = neopixel.NeoPixel(Pin(18),32)
    # print("In meter Dash")
    task2 = asyncio.create_task(line_follow(bot , ind , state, count, start_time, n, speed = 0.38))
    await asyncio.gather(task2)
            
asyncio.run(marathon())