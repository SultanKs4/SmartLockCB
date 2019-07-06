import RPi.GPIO as IO
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from gpiozero import Servo
from time import sleep

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
	if infrared == 1:
		print("Infrared Activated")
		if (IO.input(PIN_IR) == False) :
			sleep(3)
			print("Object Detected")
            sensor_ref.update({'confirm': 1})
			if servo == 1:
				print("Locker is Open")
				PIN_SERVO.max()
                sleep(60)
                PIN_SERVO.min()
                sensor_ref.update({'confirm': 0})
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