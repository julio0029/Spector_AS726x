import RPi.GPIO as GPIO
import time
import signal
import subprocess
import pygame

green_LED=24
red_LED=23
button=15

GPIO.setmode(GPIO.BCM)

GPIO.setup(green_LED, GPIO.OUT)
GPIO.setup(red_LED, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# initialise LEDs
GPIO.output(red_LED, GPIO.HIGH)
GPIO.output(green_LED, GPIO.LOW)
_RUN=0

while True:
	try:
		input_state = GPIO.input(button)
		if input_state == False and _run==0:
			p=subprocess.Popen('python /home/pi/code/Rasp_Sensor.py', shell=True)
			_RUN=1

			GPIO.output(red_LED, GPIO.LOW)
			GPIO.output(green_LED, GPIO.HIGH)

			while input_state==False:
				time.sleep(1)

		elif input_state == False and _run==1:
			p.terminate()
			 _RUN=0

			GPIO.output(red_LED, GPIO.HIGH)
			GPIO.output(green_LED, GPIO.LOW)

			while input_state==False:
				timr.sleep(1)

		time.sleep(0.2)

	except KeyboardInterrupt:
		GPIO.cleanup()


		