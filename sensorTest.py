import machine
import time
## Gives out 0 when on black surface and 1 if on white 
sensor1 = machine.Pin(4)


## Gives out 1 when on black surface and 0 if on white 
doubleSensor1 = machine.Pin(26, machine.Pin.IN)
doubleSensor2 = machine.Pin(27, machine.Pin.IN)

# sensor1.on()
# doubleSensor2.on()
# doubleSensor1.on()

#Right sensor 
print(doubleSensor1.value())
print(doubleSensor2.value())
## Left sensor 



# print(sensor1.value())


# def HCSRSensor(trigger_pin, echo_pin, ):
#     trigger = machine.Pin(trigger_pin, mode = machine.Pin.OUT,pull = None)
#     echo = machine.Pin(echo_pin, mode = machine.Pin.IN,pull = None )

#     echo_timeout_us=500*2*30

#     trigger.value(0)
#     trigger.value(1)
#     # Send a 10us pulse.
#     time.sleep_us(10)
#     trigger.value(0)

#     pulse_time = machine.time_pulse_us(echo, 1, echo_timeout_us)

#     mm  = pulse_time * 100 // 582
#     cms = (pulse_time / 2) / 29.1

#     ## Distance in millimeters
#     print(mm)

#     ## Distance in centimeter
#     print(cms)


# while True:
#     HCSRSensor(17,16)