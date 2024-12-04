import asyncio
import utime
from machine import Pin
from array import array
from main import Bot
import neopixel

p = machine.Pin(18)
n = neopixel.NeoPixel(p,32)
n[0] = (255, 0, 0)  # Set the first LED to red
n[1] = (255, 0, 0)  # Set the second LED to green


class mydistance:
    def __init__(self, echo, trigger, period_ms=100, buffer_size=10):  
        self.echo = echo
        self.trigger = trigger
        self.buffer = array('I', [0] * buffer_size)
        self.idx = 0
        self.period_ms = period_ms

    async def task(self):
        while True:
            self.trigger.low()
            utime.sleep_us(2)
            self.trigger.high()
            utime.sleep_us(5)
            self.trigger.low()
            while self.echo.value() == 0:
                signaloff = utime.ticks_us()
            while self.echo.value() == 1:
                signalon = utime.ticks_us()
            timepassed = signalon - signaloff

            val = timepassed
            self.buffer[self.idx] = val
            self.idx = (self.idx + 1) % len(self.buffer)
            await asyncio.sleep_ms(self.period_ms)

def get_distance(timepassed):
    distance = (timepassed * 0.0343)/2
    return distance


async def main():
    global bot
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
    p = Pin(18)
    n = neopixel.NeoPixel(p,32)
    # n[0] = (255, 0, 0)  # Set the first LED to red
    # n[1] = (255, 0, 0)  # Set the second LED to red
    # n.write()
    while True:
        await asyncio.sleep_ms(100)
        loop = asyncio.get_event_loop()
        distance = bot.read_distance()
        print(distance)
        #needs to change based on the distance the wall will be from the target
        distance_to_wall = 45
        if (distance <= distance_to_wall):
            bot.brakes()
            for i in range(2):
                n[i] = (0, 255, 0)
                n.write()
        else:
            n[0] = (255, 0, 0)  # Set the first LED to red
            n[1] = (255, 0, 0)  # Set the second LED to red
            n.write()
            bot.fwd()


asyncio.run(main())