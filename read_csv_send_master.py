#Import Libraries
from __future__ import print_function
import time
from RF24 import *
import RPi.GPIO as GPIO
import random
import pandas as pd
from datetime import datetime

#Load Pins
GPIO.setmode(GPIO.BCM)
#Set Pipes for listening and writing
pipes = [0xF0F0F0F0E1, 0xF0F0F0F0D2]
#Define pins used by NRF24
radio = RF24(22,1)
radio.begin()       #Start the radio
radio.setChannel(0x60) #Set channel no 60
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1, pipes[1])  #Open reading pipe to listen from master node
radio.setRetries(5, 15)
radio.openWritingPipe(pipes[0])     #Open writing pipe to send data to master node

radio.printDetails()                #Print radio details
radio.startListening()              #Start listening for commands from master node


#Create function to get the last values from the csv file using pandas library
def get_values():

    dataframe = pd.read_csv("node1_data.csv")                            #Read the csv file as pandas Dataframe

    time_stamp = dataframe['timestamp'].iloc[-1]
    temperature_value = dataframe['temperature (C)'].iloc[-1]
    temperature_value = round(temperature_value, 2)
    humidity_value = dataframe['humidity (%)'].iloc[-1]
    humidity_value = round(humidity_value, 2)
    lpg_value = dataframe['lpg (ppm)'].iloc[-1]
    lpg_value = round(lpg_value, 5)
    co_value = dataframe['carbon monoxide (ppm)'].iloc[-1]
    co_value = round(co_value, 5)
    smoke_value = dataframe['smoke (ppm)'].iloc[-1]
    smoke_value = round(smoke_value,5)
    light_value = dataframe['light (lux)'].iloc[-1]
    light_value = round(light_value, 3)
    flame_value = dataframe['flame (y/n)'].iloc[-1]
    value_list = [time_stamp, temperature_value, humidity_value, lpg_value, co_value,
                  smoke_value, light_value, flame_value]
    return value_list


#Create function to send the data to the master
def sendData(value):
    radio.stopListening()
    time.sleep(0.25)
    message = value
    print("About to send message...")
    print("value sent was " + message.decode('utf-8'))
    radio.write(message)
    radio.startListening()

#Initiate the loop
while True:
    
    while not radio.available():           #Sleep when no commmands received from master
        time.sleep(0.01)
   
   
    lenff=radio.getDynamicPayloadSize()    #set received payload to dynamic size
    receive_payload = radio.read(lenff)    #receive command payload from master
    string = receive_payload.decode('utf-8')   #decode the payload
    print('Got payload size={} command name ="{}"'.format(lenff, string))  #print the command received
    
    
    ##We want to react to the command from the master.
    sensor_values = get_values()
    command = string
    if command =="GET_TEMP":
        print("Lets get temp humdity value")
        temp = bytes((str(sensor_values[1]) + ' ' +str(sensor_values[2])), 'utf-8')   #Convert the payload to bytes format
        sendData(temp)    #send data calling the function
    elif command == "GET_GAS":
        print("Lets get Gas value")
        
        gasd = bytes((str(sensor_values[3]) + " " + str(sensor_values[4]) + " " + str(sensor_values[5])), 'utf-8')
        sendData(gasd)
    elif command == "GET_LIGHT":
        print("Lets get light value")
        
        lightt = bytes(str(sensor_values[6]), 'utf-8')
        sendData(lightt)
    elif command == "GET_FLAME":
        print("Lets get flame value.")
        
        flame_value = bytes(str(sensor_values[7]), 'utf-8')
        sendData(flame_value)
    else:
        radio.stopListening()                          #if no commands received send response to master
        radio.write(b"No commands received")
        print("We sent no commands received")
        radio.startListening()
    command = ""                                        #reset the command variable for next iteration
    

    time.sleep(1)

    
    
    
    




