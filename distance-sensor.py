from gpiozero import Device,DistanceSensor, AngularServo
from time import sleep
#from gpiozero.pins.lgpio import LGPIOFactory
#Device.pin_factory = LGPIOFactory()

from gpiozero.pins.pigpio import PiGPIOFactory
Device.pin_factory = PiGPIOFactory()

sensor = DistanceSensor(echo=23, trigger=24)
servo = AngularServo(18, max_angle=180, min_angle=-180, min_pulse_width=0.0005, max_pulse_width=0.0025)


while True:
	if sensor.distance <= 0.2:
		# print('Distance to nearest object is', sensor.distance, 'm')
		print('SERVOO!!')
		servo.angle = -20
	elif sensor.distance > 0.2:
		print('AWAY')
		servo.angle = -180
		
