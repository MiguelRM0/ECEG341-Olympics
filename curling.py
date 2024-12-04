
from machine import Pin
from array import array
from main import Bot
import neopixel

p = machine.Pin(18)
n = neopixel.NeoPixel(p,32)
n[0] = (255, 0, 0)  # Set the first LED to red
n[1] = (255, 0, 0)  # Set the second LED to green


def main():
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
    while True:
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