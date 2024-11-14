import machine
import utime
class bot:
    def __init__(self, **kwargs):
        print(kwargs)
        # setup ultrasound sensor
        self.trig = machine.Pin(kwargs["trig_pin"], machine.Pin.OUT)
        self.echo = machine.Pin(kwargs["echo_pin"], machine.Pin.IN)
        

        # Setup DC Motor pins
        self.M1A = machine.PWM(machine.Pin(kwargs["M1A"]))
        self.M1B = machine.PWM(machine.Pin(kwargs["M1B"]))
        self.M2A = machine.PWM(machine.Pin(kwargs["M2A"]))
        self.M2B = machine.PWM(machine.Pin(kwargs["M2B"]))
        self.M1A.freq(50)
        self.M1B.freq(50)
        self.M2A.freq(50)
        self.M2B.freq(50)

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


bot = bot(trig_pin = 17, echo_pin = 16, M1A = 8, M1B = 9,M2A = 11,M2B = 10 )

bot.fwd()
utime.sleep_ms(2000)
bot.leftRotate()
utime.sleep_ms(2000)
bot.rightRotate()
utime.sleep_ms(2000)
bot.brake()

# while True:
#     print(bot.read_distance())