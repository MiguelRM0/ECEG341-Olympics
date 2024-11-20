import machine
import utime
import time
class Bot:
    def __init__(self, **kwargs):
        # print(kwargs)
        # setup ultrasound sensor
        self.trig = machine.Pin(kwargs["trig_pin"], machine.Pin.OUT)
        self.echo = machine.Pin(kwargs["echo_pin"], machine.Pin.IN)
        
        #Gives value of left sensor 
        self.left = machine.Pin(27, machine.Pin.IN)
        self.right = machine.Pin(26, machine.Pin.IN)
        #Gives value of right sensor 

        self.singleSensor = machine.Pin(4)
        # Setup DC Motor pins
        self.M1A = machine.PWM(machine.Pin(kwargs["M1A"]))
        self.M1B = machine.PWM(machine.Pin(kwargs["M1B"]))
        self.M2A = machine.PWM(machine.Pin(kwargs["M2A"]))
        self.M2B = machine.PWM(machine.Pin(kwargs["M2B"]))
        self.M1A.freq(50)
        self.M1B.freq(50)
        self.M2A.freq(50)
        self.M2B.freq(50)

    def read_line(self):
        return self.left.value(), self.right.value()


    def leftRotate(self, speed = 0.3):
        self.M1A.duty_u16(0)     # Duty Cycle must be between 0 until 65535
        self.M1B.duty_u16(int(speed * 65535))
        self.M2A.duty_u16(int(speed * 65535))
        self.M2B.duty_u16(0)

    def rightRotate(self,speed = 0.3):
        self.M1A.duty_u16(int(speed * 65535))   # Duty Cycle must be between 0 until 65535
        self.M1B.duty_u16(0)
        self.M2A.duty_u16(0)
        self.M2B.duty_u16(int(speed * 65535))

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

    def read_distance(self, timeout=100):
        """Reads distance from an HC-SR04P distance sensor.
        
        2cm - 400cm range

        Args:
            trig_pin: The GPIO pin connected to the trigger pin of the sensor.
            echo_pin: The GPIO pin connected to the echo pin of the sensor.
            timeout: The maximum time (in milliseconds) to wait for a response from the sensor.

        Returns:
            The measured distance in centimeters, or None if no response was received within the timeout.
            
        Gemini
        """

        # Trigger the sensor
        self.trig.value(0)
        utime.sleep_us(2)
        self.trig.value(1)
        utime.sleep_us(10)
        self.trig.value(0)

        # Wait for the echo signal
        start_time = utime.ticks_us()
        while self.echo.value() == 0:
            signaloff = utime.ticks_us()
            if utime.ticks_diff(signaloff, start_time) > timeout * 1000:
                return None

        start_time = utime.ticks_us()
        while self.echo.value() == 1:
            signalon = utime.ticks_us()
            if utime.ticks_diff(signalon, start_time) > timeout * 1000:
                return None

        # Calculate the distance
        pulse_time = utime.ticks_diff(signalon, signaloff)
        distance = (pulse_time * 0.0343) / 2
        return distance


b = Bot(trig_pin = 16, echo_pin = 17, M1A = 8, M1B = 9,M2A = 11,M2B = 10 )

# b.fwd()

# state = 0
# count = 0
# start_time = None


# while True:
#         # state machine, wait for the line to be detected, then button press.
#         # then go straight until either sensor is 1.
#         line = b.read_line()

#         if start_time is not None and time.ticks_diff(time.ticks_ms(), start_time) > 30000:
#             print("Timeout")
#             b.stop()
#             state = 0
#             start_time = None
#             continue
    
#         if state == 0:
#             if start_time is not None:
#                 print("Run Time:", time.ticks_diff(time.ticks_ms(), start_time))
#                 start_time = None
#             if line == (1, 1):
#                 print("Ready!")
#                 state = 1
#         elif state == 1:
#             ind.toggle()
#             if line != (1,1):
#                 print("Not ready")
#                 state = 0
#             elif b.A.value() == 0:
#                 while b.A.value() == 0:
#                     time.sleep_ms(10)
#                 count = 0
#                 print("Start 3", end = "")
#                 time.sleep(1)
#                 print("2", end = "")
#                 time.sleep(1)
#                 print("1", end = "")
#                 time.sleep(1)
#                 print("Go")
#                 state = 2
#                 start_time = time.ticks_ms()
#                 b.fwd(speed=0.5)
#         elif state == 2:
#             # on line, go forward until off the line.

#             if line == (0,0):
#                 state = 3
#         elif state == 3:
#             # go forward until we see the line again.
#             # steer if one sensor is on the line.
#             if line == (1,1):
#                 count += 1
#                 if count == 7:
#                     b.stop()
#                     state = 0
#                 else:
#                     state = 2
#             elif line == (1,0):
#                 # steer left
#                 print("LEFT")
#                 b.turnleft(amount_u16=512)
#             elif line == (0,1):
#                 # steer right
#                 print("RIGHT")
#                 b.turnright(amount_u16=512)
#             else:
#                 b.fwd()
#         else:
#             raise(Exception(f"Invalid state ({state})"))
#         time.sleep_ms(0)


# b.fwd()
# utime.sleep_ms(2000)
# bot.leftRotate()
# utime.sleep_ms(2000)
# bot.rightRotate()
# utime.sleep_ms(2000)
# b.brake()

# while True:
#     print(bot.read_distance())

# while bot.singleSensor.value() == 0 and bot.doubleSensor1.value() == 0 and bot.doubleSensor2.value() == 0:
#     bot.fwd()
# while bot.singleSensor.value() == 0 and bot.doubleSensor1.value() == 1 or bot.doubleSensor2.value() == 1:
#     bot.leftRotate()
# while bot.singleSensor.value() == 0 and bot.doubleSensor1.value() == 0 and bot.doubleSensor2.value() == 0:
#     bot.fwd()

# bot.brake()