#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Collect data from Spectrophotometer
Plot live graph if option is True

Script will end if EITHER:
- graph is closed
- 
Save a csv in rt and rename 
"""

# ============ VARIABLES ==============
PLOTTING=False
AUTOADJUST=False
DEFAULT_y_lim=2000 # y limit axis if not True

import os
from global_variables import DEFAULT_PORT, TEMP_FILE, HEADERS, LED_MAP
CURRENT_PATH=os.path.dirname(os.path.abspath(__file__))	
# =====================================

from live_graph import Graph	#from this directory
from datetime import datetime
import time
from serial import Serial
from serial.tools import list_ports

from scipy.interpolate import interp1d, InterpolatedUnivariateSpline
import matplotlib.pyplot as plt
import matplotlib.colors


class Spectro():
	def __init__(self, gauge=115200):
		self.gauge=gauge
		self.data=[]
		self.reading=False
		self.plotting=False
		self.LED_MAP=LED_MAP



	def initiate_device(self, port=DEFAULT_PORT):
		# Initiate ARDUINO
		# port = DEFAULT_PORT
		# if choose_port is True:
		# 	ports=[i.device for i in list_ports.comports()]	# all available ports
		# 	print("Please choose:")
		# 	for idx, e in enumerate(ports):
		# 		print(f"{idx+1}) {e}")
		# 	i=input("Enter number: ")
			# try:
			# 	if 0 < int(i) <= len(ports):
			# 		port=ports[int(i-1)]
			# except Exception as e:print(e)
		self.port=port
		self.arduino=Serial(self.port, self.gauge)
		self.arduino.reset_input_buffer()



	def read_data(self):
		# ---- Read from ARDUINO ---
		try:
			self.lastline=self.arduino.readline().decode("utf-8")
			self.lastread=[float(d) for d in self.lastline.split(",")]
		except Exception as last_e:
			self.last_e=last_e
			print(self.last_e)

		# Skip processing if getting wrong buffer
		if(len(self.lastread)!=21):
			print("Arduino returning wrong length of data array")
			print("Skipping last read...")
			time.sleep(1)

		else:
			# Append recent data to temp.csv
			with open(TEMP_FILE,'a') as f:
				f.write(self.lastline)

			self._str=f"Time:{self.lastread[1]} | Cycle:{self.lastread[0]} | LED:{self.LED_MAP[self.lastread[2]]}"
			print(self._str)
			self.data.append(self.lastread)

			# === LIVE PLOT === :spectra last 18 values
			if self.plotting is True:
				_graph.refresh(_data[-18:], autoadjust=AUTOADJUST)
				if _graph.status is False: #if graph was closed
					self.reading=False


	def close_session(self):
		# ==== CLOSE and reset ARDUINO BUFFER
		self.arduino.reset_input_buffer()
		self.arduino.close()

		# Rename csv file
		_now=datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
		CSV_NAME=f'Spectra_{_now}.csv'
		os.rename(f"{CURRENT_PATH}/{TEMP_FILE}",
				f"{CURRENT_PATH}/DATA/{CSV_NAME}")
		print(f"Saved {CSV_NAME}\n=> EXIT")



	def run(self, rt_file=TEMP_FILE, arduino=None, plotting=False):
		self.plotting=plotting
		if self.plotting is True:
			_graph=Graph(DEFAULT_y_lim)

		with open(TEMP_FILE,'w') as f:
			f.write(f"{str(HEADERS)[1:-1]}\n")

		if arduino == None:
			self.initiate_device()
		else:self.arduino=arduino

		# MAIN LOOP ======================
		self.reading=True
		while self.reading is True:
			read_data()

		close_session()



if __name__=='__main__':
	Spectro().run(plotting=PLOTTING)

