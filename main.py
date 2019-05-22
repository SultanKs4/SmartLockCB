import RPi.GPIO as IO
import time
from firebase import firebase
from gpiozero import Servo
from time import sleep

fire = firebase.FirebaseApplication('https://smartlock-01.firebaseio.com/',None)

PIN_IR = 25
PIN_SERVO = Servo(14)

IO.setmode(IO.BCM)
IO.setup(PIN_IR, IO.IN)


while True:
	infrared=fire.get('/infra',None)
	servo2=fire.get('/servo2',None)
	if infrared == 1:
		print("Infrared Activated")
		if (IO.input(PIN_IR) == False) :
			sleep(3)
			print("Object Detected")
			if servo2 == 0 :
				print("Locker is Locked")
				PIN_SERVO.min()
			elif servo2 == 1:
				print("Locker is Open")
				PIN_SERVO.max()
			else :
				print("Enter a Valid Command")
		else:
			print("No Object Detected")
			print("Waiting 3 Second to Detect the Setting")
			print("Waiting 2 Second to Detect the Setting")
			print("Waiting 1 Second to Detect the Setting")
			sleep(3)
	else:
		print("Infra Wasnt Activated")
		print("Waiting 5 Second to Reload the Setting")
		print("Waiting 4 Second to Reload the Setting")
		print("Waiting 3 Second to Reload the Setting")
		print("Waiting 2 Second to Reload the Setting")
		print("Waiting 1 Second to Reload the Setting")
		sleep(5)