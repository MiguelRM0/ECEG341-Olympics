import asyncio
from machine import Pin
from array import array
from main import Bot


# class mydistance:
#     def __init__(self, echo, trigger, period_ms=100, buffer_size=10):  
#         self.echo = echo
#         self.trigger = trigger
#         self.buffer = array('I', [0] * buffer_size)
#         self.idx = 0
#         self.period_ms = period_ms

#     async def task(self):
#         while True:
#             self.trigger.low()
#             utime.sleep_us(2)
#             self.trigger.high()
#             utime.sleep_us(5)
#             self.trigger.low()
#             while self.echo.value() == 0:
#                 signaloff = utime.ticks_us()
#             while self.echo.value() == 1:
#                 signalon = utime.ticks_us()
#             timepassed = signalon - signaloff

#             val = timepassed
#             self.buffer[self.idx] = val
#             self.idx = (self.idx + 1) % len(self.buffer)
#             await asyncio.sleep_ms(self.period_ms)

# def get_distance(timepassed):
#     distance = (timepassed * 0.0343)/2
#     return distance


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
    while True:
        await asyncio.sleep_ms(100)
        distance = bot.read_distance()
        print(distance)
        if (distance < 75):
            bot.brakes()
        else:
            bot.fwd(speed = .9)


asyncio.run(main())
            
