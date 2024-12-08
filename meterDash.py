from bot import Bot
from machine import Pin
import neopixel
from lineFollow import line_follow
import asyncio
import sys

async def dash(bot):
    # print("In dash function")
    while True:
        distance = await bot.read_distance()
        # print(f"Distance: {distance}")
        if distance is None:
            bot.brakes()
            continue
        if (distance < 15):
            # print("Obstacle detected. Stopping bot.")
            bot.stop()
            sys.exit()
        await asyncio.sleep(0.01)

async def meterDash():
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
    task1 = asyncio.create_task(dash(bot))
    task2 = asyncio.create_task(line_follow(bot , ind , state, count, start_time, n, speed = 0.6))
    await asyncio.gather(task1,task2)
            
asyncio.run(meterDash())