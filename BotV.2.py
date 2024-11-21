import machine
import time
class bot:
    def __init__(self, **kwargs):
        # Setup DC Motor pins
        self.M1A = machine.PWM(machine.Pin(kwargs["M1A"]), freq=50, duty_u16=0)
        self.M1B = machine.PWM(machine.Pin(kwargs["M1B"]), freq=50, duty_u16=0)
        self.M2A = machine.PWM(machine.Pin(kwargs["M2A"]), freq=50, duty_u16=0)
        self.M2B = machine.PWM(machine.Pin(kwargs["M2B"]), freq=50, duty_u16=0)
        
        self.left = machine.Pin(kwargs["left"], machine.Pin.IN)
        self.right = machine.Pin(kwargs["right"], machine.Pin.IN)

        self.A = machine.Pin(kwargs["A"], machine.Pin.IN)
        self.B = machine.Pin(kwargs["B"], machine.Pin.IN)

    def read_line(self):
        return  self.left.value(),  self.right.value()

    def rotate(self, speed = 0.3):
        self.M1A.duty_u16(0)     # Duty Cycle must be between 0 until 65535
        self.M1B.duty_u16(int(speed * 65535))
        self.M2A.duty_u16(int(speed * 65535))
        self.M2B.duty_u16(0)

    def turnleft(self, amount_u16 = 0x2000):
        # turn left by increasing the speed of the right motor and decreasing the speed of the left motor
        # assumes we are going forward.
        self.M1A.duty_u16(self.M1A.duty_u16())     # Duty Cycle must be between 0 until 65535
        self.M1B.duty_u16(self.M1B.duty_u16())

        if self.M2B.duty_u16() == 0:
            # reverse
            self.M2A.duty_u16(min(0xffff,self.M2A.duty_u16() + amount_u16))
            self.M2B.duty_u16(0)
        else:
            # forward
            self.M2A.duty_u16(self.M2A.duty_u16())
            self.M2B.duty_u16(max(0,self.M2B.duty_u16() - amount_u16))

    def turnright(self, amount_u16 = 0x2000):
        # turn left by increasing the speed of the right motor and decreasing the speed of the left motor
        # assumes we are going forward.

        if self.M1B.duty_u16() == 0:
            # reverse
            self.M1A.duty_u16(min(0xffff,self.M1A.duty_u16() + amount_u16))
            self.M1B.duty_u16(0)
        else:
            # forward
            self.M1A.duty_u16(self.M1A.duty_u16())     # Duty Cycle must be between 0 until 65535
            self.M1B.duty_u16(max(0,self.M1B.duty_u16() - amount_u16))

        self.M2A.duty_u16(self.M2A.duty_u16())
        self.M2B.duty_u16(self.M2B.duty_u16())

    def stop(self):
        self.M1A.duty_u16(0)     # Duty Cycle must be between 0 until 65535
        self.M1B.duty_u16(0)
        self.M2A.duty_u16(0)
        self.M2B.duty_u16(0)

    def fwd(self, speed = 0.3):
        self.M1A.duty_u16(0)     # Duty Cycle must be between 0 until 65535
        self.M1B.duty_u16(int(speed * 65535))
        self.M2A.duty_u16(0)
        self.M2B.duty_u16(int(speed * 65535))

    def reverse(self, speed = 0.3):
        self.M1A.duty_u16(int(speed * 65535))
        self.M1B.duty_u16(0)     # Duty Cycle must be between 0 until 65535
        self.M2A.duty_u16(int(speed * 65535))
        self.M2B.duty_u16(0)

    def brake(self):
        self.M1A.duty_u16(65535)     # Duty Cycle must be between 0 until 65535
        self.M1B.duty_u16(65535)
        self.M2A.duty_u16(65535)
        self.M2B.duty_u16(65535)
        
def main():
    conf = {
        "M1A": 8,
        "M1B": 9,
        "M2A": 10,
        "M2B": 11,
        "left": 2,
        "right": 3,
        "A": 20,
        "B": 21
    }
    b = bot(**conf)

    ind = machine.Pin(0, machine.Pin.OUT)

    state = 0
    count = 0
    start_time = None


    # turn left, M1B drives the right wheel forward
    # b.M1A.duty_u16(0) 
    # b.M1B.duty_u16(0x4000)
    
    # turn right, M2B drives the left wheel forward
    # b.M2A.duty_u16(0)
    # b.M2B.duty_u16(0x4000)

    # time.sleep_ms(1000)
    # b.stop()
    


    while True:
        # state machine, wait for the line to be detected, then button press.
        # then go straight until either sensor is 1.
        line = b.read_line()

        if start_time is not None and time.ticks_diff(time.ticks_ms(), start_time) > 30000:
            print("Timeout")
            b.stop()
            state = 0
            start_time = None
            continue
    
        if state == 0:
            if start_time is not None:
                print("Run Time:", time.ticks_diff(time.ticks_ms(), start_time))
                start_time = None
            if line == (1, 1):
                print("Ready!")
                state = 1
        elif state == 1:
            ind.toggle()
            if line != (1,1):
                print("Not ready")
                state = 0
            elif b.A.value() == 0:
                while b.A.value() == 0:
                    time.sleep_ms(10)
                count = 0
                print("Start 3", end = "")
                time.sleep(1)
                print("2", end = "")
                time.sleep(1)
                print("1", end = "")
                time.sleep(1)
                print("Go")
                state = 2
                start_time = time.ticks_ms()
                b.fwd(speed=0.5)
        elif state == 2:
            # on line, go forward until off the line.

            if line == (0,0):
                state = 3
        elif state == 3:
            # go forward until we see the line again.
            # steer if one sensor is on the line.
            if line == (1,1):
                count += 1
                if count == 7:
                    b.stop()
                    state = 0
                else:
                    state = 2
            elif line == (1,0):
                # steer left
                print("LEFT")
                b.turnleft(amount_u16=512)
            elif line == (0,1):
                # steer right
                print("RIGHT")
                b.turnright(amount_u16=512)
            else:
                b.fwd()
        else:
            raise(Exception(f"Invalid state ({state})"))
        time.sleep_ms(0)

try:
    main()
except Exception as e:
    conf = {
        "M1A": 8,
        "M1B": 9,
        "M2A": 10,
        "M2B": 11,
        "left": 2,
        "right": 3,
        "A": 20,
        "B": 21
    }
    b = bot(**conf)
    b.stop()
    print("Emergency stop.")
    raise(e)
