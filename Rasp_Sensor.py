import RPi.GPIO as GPIO
import time, board, datetime
from adafruit_as726x import AS726x_I2C

# ============= PARAMETERS ============
BUTTON_PRESSED=False
SPECTRA_PERIOD = 5 #s
DATAPATH='/home/pi/data'

# Define leds and corresponding ports
LEDs={
	0:4,
	385:5,
	400:6,
	455:13,
	557:19,
	660:26}

# ==== Setup =====
# -- LEDs
GPIO.setmode(GPIO.BCM)
for _, led in LEDs.items():
	GPIO.setup(led, GPIO.OUT)

# -- Sensor
i2c = board.I2C()
sensor=AS726x_I2C(i2c)
sensor.conversion_mode=sensor.MODE_2
print(f"Temp: {sensor.temperature}")



def averaged_spectra(period=1, _delta=0.1):
	# By default will collect data every 100ms
	data={450:[], 500:[], 550:[], 575:[], 600:[], 650:[]}

	_start=time.time()
	deltaT=float(period-float(time.time()-_start)-_delta)

	while deltaT>0:
		try:
			if sensor.data_ready:
				mapping={
					450:sensor.violet,
					500:sensor.blue,
					550:sensor.green,
					575:sensor.yellow,
					600:sensor.orange,
					650:sensor.red}
				
				for nm, _sens in mapping.items():
					data[nm].append(_sens)
 
		except Exception as e:
			 print(e)
		 
		# Get remaining time
		time.sleep(_delta)
		deltaT=float(period-float(time.time()-_start)-_delta)
	# print(f"Averaged: {len(data[450])} spectra")
	# Average data
	for nm, lst in data.items():
		data[nm] = sum(data[nm])#/len(data[nm])
	
	return data

	
def sum_spectra(_count=4):
	# By default will collect data every 100ms
	data={450:[], 500:[], 550:[], 575:[], 600:[], 650:[]}
	c=0
	while c<=_count:
		try:
			while not sensor.data_ready:
				time.sleep(0.1)
			mapping={
					450:sensor.violet,
					500:sensor.blue,
					550:sensor.green,
					575:sensor.yellow,
					600:sensor.orange,
					650:sensor.red}
				
			for nm, _sens in mapping.items():
				data[nm].append(float(_sens))
 
		except Exception as e:
			 print(e)
		c+=1

	# Average data
	for nm, lst in data.items():
		data[nm] = sum(data[nm])
	
	return data    


def q_press():
	_quite=False
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				_quite=True
	if _quite is True:
		print("Exit")
	GPIO.cleanup()
	exit()


def record_data(filename, cycle):

	for nm, led in LEDs.items():
		#print(f"{nm}nm ON")
		GPIO.output(led, GPIO.HIGH)

		# Wait for data to be ready
		while not sensor.data_ready:
			time.sleep(0.1)
		
		# get spectra over 1s average
		data=sum_spectra(_count=SPECTRA_PERIOD)
		data.update({'nm':nm})
		
		#Append to file
		# Open file to append
		with open(filename, 'a') as f:
			f.write(f"{str(data)},")

		GPIO.output(led, GPIO.LOW)
		
			



def main():
	

	while BUTTON_PRESSED is False:
		time.sleep(1)

	# Start sensor
	time.sleep(0.5)
	filename=f"{DATAPATH}/spectra_{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.csv"
	_cycle=0


	while BUTTON_PRESSED is True:
		try:
			record_data(filename=filename, cycle=_cycle)
			_cycle+=1
		except KeyboardInterrupt:
			GPIO.cleanup()


	
	
if __name__ == "__main__":
	main()
	