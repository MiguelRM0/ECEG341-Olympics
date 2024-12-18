
from bot import Bot
from machine import Pin
import neopixel
from lineFollow import Follow
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
bot.set_speed(0)
bot.fwd()
