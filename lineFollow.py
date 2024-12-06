from main import Bot
import time
import machine
import neopixel

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
    b = Bot(**conf)

    ind = machine.Pin(0, machine.Pin.OUT)

    state = 0
    count = 0
    start_time = None
    n = neopixel.NeoPixel(machine.Pin(18),32)
    line_follow(b, ind, state, count, start_time, n)

def line_follow(b, ind, state, count, start_time, n):
    while True:
        # state machine, wait for the line to be detected, then button press.
        # then go straight until either sensor is 1.
        line = b.read_line()
        print(line)

        if start_time is not None and time.ticks_diff(time.ticks_ms(), start_time) > 100000000000:
            b.stop()
            state = 0
            start_time = None
            continue

        if state == 0:
            n[0] = (255,0,255)
            n[1] = (255,0,255)
            n.write()
            if start_time is not None:
                start_time = None
            if line == (0, 0):
                state = 1
        elif state == 1:
            ind.toggle()
            n[0] = (255,0,0)
            n[1] = (255,0,0)
            n.write()
            if line != (0,0):
                state = 0
            elif b.A.value() == 0:
                while b.A.value() == 0:
                    time.sleep_ms(10)
                count = 0
                time.sleep(1)
                time.sleep(1)
                time.sleep(1)
                state = 2
                start_time = time.ticks_ms()
                b.fwd()
        elif state == 2:
            n[0] = (0,255,0)
            n[1] = (0,255,0)
            n.write()
            # on line, go forward until off the line.
            if line == (0,0):
                state = 3
            
            
        elif state == 3:
            n[0] = (0,0,255)
            n[1] = (0,0,255)
            n.write()
            # go forward until we see the line again.
            # steer if one sensor is on the line.
            if line == (1,1):
                b.turnleft()
            elif line == (1,0):
                # steer left
                b.turnleft(amount_u16=512)
            elif line == (0,1):
                # steer right
                b.turnright(amount_u16=512)
            else:
                b.fwd()
        else:
            raise(Exception(f"Invalid state ({state})"))
        time.sleep_ms(0)

try:
    main()
except Exception as e:
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
    b = Bot(**conf)
    b.stop()
    raise(e)
# # turn left, M1B drives the right wheel forward
# b.M1A.duty_u16(0) 
# b.M1B.duty_u16(0x4000)
    
#     # turn right, M2B drives the left wheel forward
# b.M2A.duty_u16(0)
# b.M2B.duty_u16(0x4000)

# time.sleep_ms(1000)
# b.brake()