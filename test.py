print("Hello World")

print("Hello World")



import machine
import time


print("hello")

M2A = machine.Pin(10)
M2B = machine.Pin(11)

M1A = machine.PWM(machine.Pin(8),freq = 50, duty_u16 = 0)
M1B = machine.PWM(machine.Pin(9), freq = 50, duty_u16 = int(65535 * 0.50))
M2A = machine.PWM(machine.Pin(10), freq = 50, duty_u16 = int(65535 * 0.50))
M2B = machine.PWM(machine.Pin(11), freq = 50, duty_u16 = 0)
time.sleep_ms(10)

M1A 
M1B
M2A
M2B
