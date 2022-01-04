import socket
import csv
import numpy as np
import serial

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

arduino = serial.Serial('COM3',9600) #set arduino serial port
arduino.write("0900090".encode())

sock.connect(("10.123.166.227", 6000))
ALL = []
title = ['x_Raw','y_Raw','z_Raw','x_Gravity','y_Gravity','z_Gravity',
         'x_Linear','y_Linear','z_Linear','x_Gyroscope','y_Gyroscope',
         'z_Gyroscope','x_Geomagnetic','y_Geomagnetic','z_Geomagnetic',
         #'x_Pitch','y_Roll','x_Yaw',
         'rotationMatirx0','rotationMatirx1',
         'rotationMatirx2','rotationMatirx3','rotationMatirx4',
         'rotationMatirx5','RrotationMatirx','rotationMatirx7',
         'rotationMatirx8']
ALL.append(title)
nor0 = np.array([[0],[0],[-1]])
dc1 = 0
dc3 = 0
angle_title = ['roatation_x','rotation_y','rotation_x_temp','rotation_y_temp']
ra=[]
ra.append(angle_title)
count = 0
while count<300:
    print(count)
    #read data from phone
    msg = sock.recv(512)
    msg = msg[2:]
    try:
        msg = msg.decode("utf-8")
        msg = msg.split(",")
        if len(msg)!=24:
            msg = ''
        if (msg!=''):
            #print(msg)
            ALL.append(msg)
            aa = msg[-9:]
            for i in range(len(aa)):
                aa[i] = float(aa[i])
            RotationMatrix = np.array(aa).reshape((3,3))
            #print(RotationMatrix)
            nor = np.matmul(RotationMatrix,nor0)
            if count>0:
                dc1_temp = (np.arctan(nor[2]/nor[1])/np.pi*180-c1)
                dc3_temp = (np.arctan(-nor[0]/nor[1])/np.pi*180-c3)
                dc1 += dc1_temp[0]
                dc3 += dc3_temp[0]               
                ra.append((dc1,dc3,dc1_temp[0],dc3_temp[0]))
                rotation_x = 90 - dc1
                rotation_y = 90 - dc3
                print("rotation_x = " + str(rotation_x))
                print("rotation_y = " + str(rotation_y))
                if rotation_x >=60 and rotation_x <=175 and rotation_y >= 0 and rotation_y <=175 :
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
            c1 = np.arctan(nor[2]/nor[1])/np.pi*180
            c3 = np.arctan(-nor[0]/nor[1])/np.pi*180
            
            count += 1
    except:
        print("read fail")


with open('Readings.csv', 'wt', newline='') as f:
    writer = csv.writer(f,delimiter = ',')
    writer.writerows(ALL)
    
with open('ServoInputs.csv', 'wt', newline='') as f:
    writer = csv.writer(f,delimiter = ',')
    writer.writerows(ra)




