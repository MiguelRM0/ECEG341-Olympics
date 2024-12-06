import asyncio
from machine import Pin
from array import array
from main import Bot
import neopixel
from lineFollow import line_follow

async def dash(bot):
    while True:
        distance = await asyncio.to_thread(bot.read_distance)
        if distance == None:
            bot.brakes()
            continue
        if (distance < 20):
            bot.brakes()
            await asyncio.sleep_ms(100)
        else:
            bot.fwd(speed = .9)
            await asyncio.sleep_ms(100)

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
    loop = asyncio.get_event_loop()
    loop.create_task(dash(bot))
    loop.create_task(asyncio.to_thread(line_follow, state, count, start_time, n))
    await asyncio.gather()
            
asyncio.run(main())