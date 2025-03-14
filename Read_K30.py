# -*- coding: utf-8 -*-
"""
Oroginally created on Tue Jan 30 15:08:39 2024

@author: Julien Hacot-Slonosky


Updated on Tue Jul  2 13:10:52 2024

@author: Julien Hacot-Slonosky


This script is used to read serial data coming out of an Arduino and save the
data in a text file delimeted by a comma.

"""

import serial
import time
import os

arduino = serial.Serial(port='COM11', baudrate = 9600)  # open the arduino

time.sleep(2)  # wait for the arduino to go through it's startup cycle

t_end = time.time() + 60*15  # end time in seconds

hum_l = []
t_elapsed_l = []

os.chdir(r"C:\Users\merry\OneDrive\Documents\McGill\U3\Robotics")

filename = "CO2_test_3.txt"  # filename to output

mess_in_progress = False
message=""  # dont reset the message at the beginning of the loop you doofus

while time.time() < t_end or arduino.in_waiting > 0 or mess_in_progress:
   
    rc = arduino.read().decode('utf-8')  #recieved character in the serial port
    print(rc)
    if mess_in_progress == True:
        if rc != ">":  # if the message is not the end character
            message = ''.join([message, rc])  # keep updating the message
            print(message)
        elif rc == ">":  # if the end character is read
            mess_in_progress = False
            vals = message.split(",")  # split the message along the commas
            #print(vals)
            if len(vals) > 1:  # to make sure that no empty messages pass
                conf = vals[0]
                co2 = float(vals[1])
                #temp = float(vals[2])
                #hum_l.append(humidity)
                #t_elapsed_l.append(dht_temp)
                # write into the file, keep appending to it
                file = open(filename, 'a')
                file.write(str(co2)+"\n")
                file.close()
                message = ""  # reset the message
    elif rc == "<":  # if the start characer is read, begin reading the message
        mess_in_progress = True
            

        

arduino.close()

print("Message read complete.")
