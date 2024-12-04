import machine
import utime
import asyncio
class Bot:
    def __init__(self, **kwargs):
        # print(kwargs)
        # setup ultrasound sensor
        self.trig = machine.Pin(kwargs["trig_pin"], machine.Pin.OUT)
        self.echo = machine.Pin(kwargs["echo_pin"], machine.Pin.IN)
        
        #Gives value of left sensor 
        # self.left = machine.Pin(27, machine.Pin.IN)
        # self.right = machine.Pin(26, machine.Pin.IN)
        #Gives value of right sensor 

        self.left = machine.Pin(kwargs["left_sensor"], machine.Pin.IN)
        self.right = machine.Pin(kwargs["right_sensor"], machine.Pin.IN)


        self.A = machine.Pin(kwargs["A"], machine.Pin.IN)
        self.B = machine.Pin(kwargs["B"], machine.Pin.IN)

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
            
    
    def turnright(self, amount_u16 = 0x2000):
        # turn left by increasing the speed of the right motor and decreasing the speed of the left motor
        # assumes we are going forward.

        if self.M1B.duty_u16() == 0:
            # reverse
            self.M1A.duty_u16(min(0xffff,self.M1A.duty_u16() + amount_u16))
            self.M1B.duty_u16(0)
        else:
            # forwardç
            self.M1A.duty_u16(self.M1A.duty_u16())     # Duty Cycle must be between 0 until 65535
            self.M1B.duty_u16(max(0,self.M1B.duty_u16() - amount_u16))

        self.M2A.duty_u16(self.M2A.duty_u16())
        self.M2B.duty_u16(self.M2B.duty_u16())



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

    def brakes(self):
        self.M1A.duty_u16(65535)     # Duty Cycle must be between 0 until 65535
        self.M1B.duty_u16(65535)
        self.M2A.duty_u16(65535)
        self.M2B.duty_u16(65535)

    def stop(self):
        self.M1A.duty_u16(0)     # Duty Cycle must be between 0 until 65535
        self.M1B.duty_u16(0)
        self.M2A.duty_u16(0)
        self.M2B.duty_u16(0)


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
    

# import curling # Import the main function from followLine.py
# asyncio.run(curling.main())  # Call the main function
    
# if __name__== "__main__":
#     from meterDash import main 
#     asyncio.run(main)

# if __name__== "__main__":
#     from curling import main
#     asyncio.run(main())
# if __name__ == "__main__":
#     from lineFollow import main
#     main
