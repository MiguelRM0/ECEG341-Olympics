import asyncio
from os import utime
from machine import Pin
from array import array
from bot import *
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
    bot = Bot(trig_pin = 17, echo_pin = 16, M1A = 8, M1B = 9,M2A = 11,M2B = 10, A = 20, B = 21)
    while True:
        await asyncio.sleep_ms(100)
        loop = asyncio.get_event_loop()
        distance_read = mydistance(Pin(16, Pin.IN),Pin(17, Pin.OUT))
        distance = get_distance(sum(distance_read.buffer) // len(distance_read.buffer))
        loop.create_task(distance_read.task())
        #needs to change based on the distance the wall will be from the target
        distance_to_wall = 45
        if (distance <= distance_to_wall):
            bot.breaks()
            for i in range(2):
                n[i] = (0, 255, 0)
                n.write()
        else:
            bot.fwd(speed = .2)