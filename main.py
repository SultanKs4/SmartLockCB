import RPi.GPIO as IO
import time
import ast
import firebase_admin
import firebase_cred
from firebase_admin import credentials
from firebase_admin import firestore
from gpiozero import Servo
from time import sleep

collection = firebase_cred.smart_lock_col

PIN_IR = 25
PIN_SERVO = Servo(14)

IO.setmode(IO.BCM)
IO.setup(PIN_IR, IO.IN)


while True:
	sensor_ref = collection.document(u'sensor')
	sensors = sensor_ref.get()
	sensors_string_dict = '{}'.format(sensors.to_dict())
	sensors_dict = ast.literal_eval(sensors_string_dict)
	confirm = sensors_dict['confirm']
	infrared = sensors_dict['infrared']
	servo = sensors_dict['servo']
	command = sensors_dict['command']
	if infrared == 1:
		#sensor_ref.update({'infrared': 1})
		#sensor_ref.update({'servo': 1})
		print("Infrared Activated")
		sleep(2)
		if (IO.input(PIN_IR) == False) :
			print("Object Detected")
			sensor_ref.update({'confirm': 1})
			sleep(3)
			if servo == 1:
				print("Locker is Open")
				PIN_SERVO.max()
				sensor_ref.update({'infrared': 0})
				sleep(10)
		else:
			print("No Object Detected")
			print("Waiting 3 Second to Detect the Setting")
			sleep(3)
	elif command == "lock":
		sensor_ref.update({'confirm': 0,'servo': 0})
		PIN_SERVO.min()
		print("Locker is Locked")
		sensor_ref.update({u'command' : u'locked'})
