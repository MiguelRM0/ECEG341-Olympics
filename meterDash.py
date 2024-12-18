import asyncio
from bot import Bot
from machine import Pin
import neopixel
from lineFollow import line_follow

async def dash(bot, speed_container):
    while True:
        distance = bot.read_distance()
        # print(distance)
        if distance is None:
            bot.stop()
            speed_container[0] = 0
            continue
        if distance < 10:
            # bot.stop()
            speed_container[0] = 0  # Set speed to 0 to stop the bot
        elif distance >= 10:
            speed_container[0] = 0.65
        await asyncio.sleep(0.01)

async def meterDash():
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

    # Use a mutable container for speed
    speed_container = [0.65]  # Initial speed

    # Start tasks with shared speed_container
    task2 = asyncio.create_task(line_follow(bot, ind, state, count, start_time, n, speed_container))
    task1 = asyncio.create_task(dash(bot, speed_container))

    await asyncio.gather(task1, task2)

asyncio.run(meterDash())
