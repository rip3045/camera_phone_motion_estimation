
import socket 
import numpy as np
from numpy import linalg as LA
import math
import csv
import serial
from scipy.signal import butter, filtfilt, freqz
import statistics
import time
from time import sleep
import os
#os.system("clear")


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

arduino = serial.Serial('COM5',9600) #set arduino serial port
arduino.write("0900090".encode())


sock.connect(("10.123.144.85", 6000))


#create a lowpass filter 
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a
def butter_lowpass_filter(data, cutoff, fs, order = 5):
    b, a = butter_lowpass(cutoff, fs, order = order)
    y = filtfilt(b,a,data)
    return y

v1 = np.array([0.00005,0,0]) #initial_velocities
e_previous = np.identity(3) #initial_frame as reference_frame
R = np.identity(3) #initial transformation matrix is identity matrix

count = 0
accel_readings_previous = ""
a_data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
sample_size = 1 # set sample_size larger than 25 to make the filter works well
dt = 0.05 #time for one sample
fs = 20 #sampling frequency
cutoff = 4 #lowpass cutoff frequency
ALL = [] #save all wanted variables into a list
sample_data = [] #save one sample data into a list
acc_reading = [] #save the accelerometer readings
while count<80:
	if count == 0:
		print("###################=====Begin!====###################")
    #read data from phone
	msg = sock.recv(128)
	msg = msg.decode("utf")
	msg = msg[2:]
	msg = msg.split(",")
	if len(msg)>6: 
		msg =""
	if (msg!='' and msg != accel_readings_previous and len(msg)==6):
		for i in range(len(a_data)):
			a_data[i] = float(msg[i])
		accel_readings_data = np.array(a_data) #acceleration readings of current time stamp, float array
		acc_reading.append(accel_readings_data)
		at = a_data[0]
		an = a_data[2]
		#ab = -a_data[1]
		ab = 0
		a = np.array([at,an,ab])
		a_abs = np.dot(R,a)
		#print(a_abs)
		#print(LA.norm(a_abs))
		v2 = v1 + a_abs*dt
		ds = LA.norm(v2)
		dr = v2
		ddr = a_abs
		et = v2/ds
		en = (ds**2*ddr-dr*np.matmul(dr,ddr))/(ds*math.sqrt(np.matmul(ddr,ddr)*(ds**2)-(np.matmul(dr,ddr))**2))
		eb = np.cross(et,en)
		e_now = np.array([et,en,eb])
		R_r = np.dot(e_previous,e_now.T)
		R = np.dot(R,R_r)
		#print(R_r)             
		if count > 40:
			#rotation_x = 90 - (int(np.arctan2(v2[2],v2[1]) * 180 / np.pi))
			rotation_x = 90
			rotation_y = 90 + (int(np.arctan2(v2[1],v2[0]) * 180 / np.pi))
			#print("rotation_x = " + str(rotation_x))
			print("rotation_y = " + str(rotation_y))
			if rotation_y >=90 and rotation_y <=175 and rotation_x >= 40 and rotation_x <=175 :
				if len(str(rotation_x)) != 3:
					rotation_x = "%03d" % rotation_x
				if len(str(rotation_y)) != 3:
					rotation_y = "%03d" % rotation_y
				rotation = (str(rotation_x)+'0'+str(rotation_y))
				print(rotation)
				#send the calculated positions to arduino
				arduino.write(rotation.encode())        
			else:
				print("Servos input wrong!")
				#break
			ALL.append(np.hstack((a,0,a_abs,0,v2,0,ds,0,rotation_x,0,rotation_y)))  
			
			v1=v2
			e_previous = e_now
			#time.sleep(0.2)
			sample_data = []
	count += 1
    
arduino.write("0900090".encode())

with open('result.csv', 'wt', newline='') as f:
    writer = csv.writer(f,delimiter = ',')
    writer.writerows(ALL)
    
    

    
