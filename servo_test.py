from gpiozero import AngularServo,Device 
from time import sleep
# from gpiozero.pins.pigpio import PiGPIOFactory
# Device.pin_factory = PiGPIOFactory()
# import pigpio
from gpiozero.pins.lgpio import LGPIOFactory

Device.pin_factory = LGPIOFactory()

# pin_factory = PiGPIOFactory()
servo = AngularServo(18, max_angle=180, min_angle=-180, min_pulse_width=0.0005, max_pulse_width=0.0025)

while True:
    servo.angle = -180
    sleep(2)
    servo.angle = 180
    sleep(2)