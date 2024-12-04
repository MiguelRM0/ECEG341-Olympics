
from machine import Pin
from array import array
from main import Bot



def main():
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
        distance = bot.read_distance()
        print(distance)
        if (distance < 75):
            bot.brakes()
        else:
            bot.fwd(speed = .9)
            
