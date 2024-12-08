"""
Breaking portion of the ECEG341 Robot Olympics
11/18/2024
Mike Merola and Miguel Romero
"""

import asyncio
from machine import Pin,PWM
import time
import random
from bot import Bot
import utime
from time import sleep_ms
import neopixel

buzzer = PWM(Pin(22))
#notes that can be used
tones = {
"B0": 31,"C1": 33,"CS1": 35,"D1": 37,"DS1": 39,"E1": 41,"F1": 44,"FS1": 46,
"G1": 49,"GS1": 52,"A1": 55,"AS1": 58,"B1": 62,"C2": 65,
"CS2": 69,"D2": 73,"DS2": 78,"E2": 82,"F2": 87,"FS2": 93,"G2": 98,
"GS2": 104,"A2": 110,"AS2": 117,"B2": 123,"C3": 131,"CS3": 139,
"D3": 147,"DS3": 156,"E3": 165,"F3": 175,"FS3": 185,
"G3": 196,"GS3": 208,"A3": 220,"AS3": 233,"B3": 247,"C4": 262,"CS4": 277,"D4": 294,"DS4": 311,
"E4": 330,"F4": 349,"FS4": 370,"G4": 392,"GS4": 415,"A4": 440,"AS4": 466,"B4": 494,"C5": 523,"CS5": 554,"D5": 587,"DS5": 622,"E5": 659,"F5": 698,
"FS5": 740,"G5": 784,"GS5": 831,"A5": 880,"AS5": 932,"B5": 988,"C6": 1047,"CS6": 1109,"D6": 1175,"DS6": 1245,"E6": 1319,"F6": 1397,"FS6": 1480,"G6": 1568,"GS6": 1661,
"A6": 1760,"AS6": 1865,"B6": 1976,"C7": 2093,"CS7": 2217,"D7": 2349,"DS7": 2489,"E7": 2637,"F7": 2794,"FS7": 2960,"G7": 3136,"GS7": 3322,"A7": 3520,
"AS7": 3729,"B7": 3951,"C8": 4186,"CS8": 4435,"D8": 4699,"DS8": 4978
}

#Take on me by A-ha 
take_on_me = [
    "E5", "E5", "E5", "P", "E5", "G5", "A5", "A5", "A5", "E5", "G5", "A5", "P",
    "E5", "G5", "A5", "A5", "A5", "G5", "P", "E5", "G5", "A5", "P", "E5", "G5", "A5",
    "E5", "G5", "A5", "A5", "A5", "G5", "P", "E5", "G5", "A5", "P", "E5", "G5", "A5",
    "A5", "A5", "G5", "P", "A5", "G5", "E5", "G5", "A5", "A5", "A5", "G5"
]

def playtone(frequency):
    buzzer.duty_u16(1<<14)
    buzzer.freq(frequency)

def bequiet():
    buzzer.duty_u16(0)

async def playsong(mysong):
    for i in range(len(mysong)):
        if (mysong[i] == "P" or mysong[i] == 0 ):
            bequiet()
        else:
            playtone(tones[mysong[i]])
        await asyncio.sleep_ms(225)
    bequiet()


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

def get_type_ground1():
    if bot.right.value() == 0:
        return 0
    else:
        return 1
    
def get_type_ground2():
    if bot.left.value() == 0:
        return 0
    else:
        return 1
    
#checks to make sure the bot hasn't detected the border
async def check_border():
    print("in check_border")
    while True:
        if (get_type_ground1() == 1 or get_type_ground2() == 1):
            await adjust_position()
        await asyncio.sleep_ms(100)

async def movement():
    # print("in movement")
    bot.fwd(speed = .5)
    await asyncio.sleep_ms(100)
    bot.rightRotate(speed =.3)
    time = random.randint(200, 3000) 
    # print(time)
    await asyncio.sleep_ms(time)
    bot.leftRotate(speed = .5)
    time2 = random.randint(200, 3000) 
    # print(time2)
    await asyncio.sleep_ms(time2)
    
async def adjust_position():
    # print("in adjust position")
    #if the bot is too close to the edge it should then reverse and rotate left to face a new direction
    bot.reverse()
    await asyncio.sleep_ms(1000)
    bot.leftRotate()
    time = random.randint(200, 3000) 
    # print(time)
    await asyncio.sleep_ms(time)

async def light_show():
    while True:
        rand1 = random.randint(0, 255)
        rand2 = random.randint(0, 255)
        rand3 = random.randint(0, 255)
        n[0] = (rand1, rand2, rand3)
        n[1] = (rand3, rand2, rand1)
        n.write()
        await asyncio.sleep_ms(1000)

async def main_function():
    asyncio.create_task(check_border())
    asyncio.create_task(light_show())
    asyncio.create_task(playsong(take_on_me)) 
    #plays the song
    
    #cycles the lights on the board

    start_time = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_time) < 30000:
        # playsong(take_on_me)
        await movement()
        await asyncio.sleep_ms(100)
    bot.stop()

asyncio.run(main_function())
