from main import Bot
from machine import Pin
import neopixel
from lineFollow import line_follow
import asyncio

async def dash(bot):
    while True:
        distance = await asyncio.to_thread(bot.read_distance)
        if distance is None:
            bot.brakes()
            continue
        if (distance < 20):
            bot.brakes()
            await asyncio.sleep_ms(100)
        else:
            bot.fwd(speed = .9)
            await asyncio.sleep_ms(100)

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
    n = neopixel.NeoPixel(machine.Pin(18),32)
    task1 = asyncio.create_task(dash(bot))
    task2 = asyncio.create_task(asyncio.to_thread(line_follow, state, count, start_time, n))
    await asyncio.gather(task1,task2)
            
# asyncio.run(meterDash())