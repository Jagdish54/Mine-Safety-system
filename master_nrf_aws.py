from __future__ import print_function
import time
from RF24 import *
import RPi.GPIO as GPIO
import csv
from datetime import datetime


# importing libraries for AWS
import paho.mqtt.client as paho
import os
import socket
import ssl
import json

##AWS CODE##################
connflag = False
 
def on_connect(client, userdata, flags, rc):                # func for making connection
    global connflag
    print ("Connected to AWS")
    connflag = True
    print("Connection returned result: " + str(rc) )
 
def on_message(client, userdata, msg):                      # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))

# get the MAC address of the specified interface

mac_ID = open('/sys/class/net/eth0/address').read()
mac_ID = mac_ID[0:17]
  

 
#def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))
 
mqttc = paho.Client()                                       # mqttc object
mqttc.on_connect = on_connect                               # assign on_connect func
mqttc.on_message = on_message                               # assign on_message func
#mqttc.on_log = on_log

#### Change following parameters #### 
awshost = "a2rsayzddbe2ho-ats.iot.ap-southeast-2.amazonaws.com"      # Endpoint
awsport = 8883                                              # Port no.   
clientId = "TestCoalClient"                                     # Thing_Name
thingName = "TestCoalThing"                                    # Thing_Name
caPath = "/home/pi/Downloads/AWSCerts/AmazonRootCA1.pem" # Root_CA_Certificate_Name
certPath = "/home/pi/Downloads/AWSCerts/9b7668b247-certificate.pem.crt"                            # <Thing_Name>.cert.pem
keyPath = "/home/pi/Downloads/AWSCerts/9b7668b247-private.pem.key"                          # <Thing_Name>.private.key
 
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters
 
mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server
 
mqttc.loop_start()                                          # Start the loop



#####NRF24 Code#############
GPIO.setmode(GPIO.BCM)

pipes = [0xF0F0F0F0E1, 0xF0F0F0F0D2]

radio = RF24(22,0)
radio.begin()

min_payload_size = 4

max_payload_size = 128
payload_size_increments_by = 1

next_payload_size = min_payload_size
millis = lambda: int(round(time.time() * 1000))

#radio.setPayloadSize(32)
radio.setChannel(0x60)
#radio.setPALevel(RF24.PA_MIN)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1, pipes[0])
radio.openWritingPipe(pipes[1])

radio.setRetries(5, 15)

radio.printDetails()
#radio.startListening()

def receiveData():
    global string
    print("Ready to receive Data")
    radio.startListening()
    while not radio.available():
        time.sleep(1/100)
    lengg = radio.getDynamicPayloadSize()
    receivedPayload = radio.read(lengg)
    string = receivedPayload.decode('utf-8')
    print("Got Payload of Size = {}".format(lengg))
    print("Payload Mesage from slave was = {}".format(string))
    radio.stopListening()

def convert(string):
    li = list(string.split(" "))
    return li

def main():
    while True:
        command = [b"GET_TEMP", b'GET_GAS', b'GET_LIGHT', b'GET_FLAME']

        global timestamp_string
        global temp_received
        global gas_received
        global light_received
        global flame_received

        for x in range(0,4):
            radio.write(command[x])
            print ("We sent the message of {}.".format(command[x]))


        #check if it returnes a _FLAME
            radio.startListening()


     # Wait here until we get a response, or timeout

            started_waiting_at = millis()

            timeout = False

            while (not radio.available()) and (not timeout):

                    if (millis() - started_waiting_at) > 500:

                        timeout = True


            if timeout:

                print('failed, response timed out.')
                while timeout:
                    main()


            else:
                # Grab the response, compare, and send to debugging spew
                receiveData()
                if command[x] == b"GET_TEMP":
                    temp_received = string
                    temp_hum_list = convert(temp_received)
                    temp = float(temp_hum_list[0])
                    humidity = float(temp_hum_list[1])

                elif command[x] == b"GET_GAS":
                    gas_received = string
                    gas_list = convert(gas_received)
                    lpg = float(gas_list[0])
                    carb_mono = float(gas_list[1])
                    smoke = float(gas_list[2])

                elif command[x] == b"GET_LIGHT":
                    light_received = string
                    light_received = convert(light_received)
                    light_received = float(light_received[0])
                elif command[x] == b"GET_FLAME":
                    flame_received = string
                    flame_received = convert(flame_received)
                    flame_received = int(flame_received[0])
                else:
                    print("No commands received to write in csv")

                now_time = datetime.now()
                timestamp_string = now_time.strftime("%d-%m-%Y %H:%M:%S")
                time.sleep(1)
                
        if connflag == True:
            macIdStr = mac_ID
       
            paylodmsg0="{"
            paylodmsg1 = "\"mac_Id\": \""
            paylodmsg2 = "\", \"1.time_stamp\": \""  
            paylodmsg3 = "\", \"2.temperature(C)\":"
            paylodmsg4 = ", \"3.Humidity (%)\":"
            paylodmsg5 = ", \"4.LPG (ppm)\":"
            paylodmsg6 = ", \"5.CO (ppm)\":"
            paylodmsg7 = ", \"6.Smoke (ppm)\":"
            paylodmsg8 = ", \"7.Light (lux)\":"
            paylodmsg9 = ", \"8.Flame (1/0)\":"
            paylodmsg10="}"
            paylodmsg = "{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(paylodmsg0, paylodmsg1, macIdStr,
                                                     paylodmsg2, timestamp_string,
                                                     paylodmsg3, temp,
                                                     paylodmsg4, humidity,
                                                     paylodmsg5, lpg,
                                                     paylodmsg6, carb_mono,
                                                     paylodmsg7, smoke,
                                                     paylodmsg8, light_received,
                                                     paylodmsg9, flame_received,
                                                     paylodmsg10)
            paylodmsg = json.dumps(paylodmsg) 
            paylodmsg_json = json.loads(paylodmsg)       
            mqttc.publish("MyCoalTest", paylodmsg_json , qos=1)        # topic: temperature # Publishing Temperature values
            print("msg sent: MyCoalTest" ) # Print sent temperature msg on console
            print(paylodmsg_json)

        else:
            print("waiting for connection to AWS...")        
                  
                
                
        with open('received_value_numbers.csv', 'a', newline ='') as csvfile:
            fieldnames = ['timestamp',
                          'temperature (C)',
                          'humidity (%)',
                          'lpg (ppm)',
                          'carbon monoxide (ppm)',
                          'smoke (ppm)',
                          'light (lumens)',
                          'flame (y/n)']

            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)

            writer.writerow({'timestamp': timestamp_string,
                             'temperature (C)' : temp,
                             'humidity (%)' : humidity,
                             'lpg (ppm)': lpg,
                             'carbon monoxide (ppm)': carb_mono,
                             'smoke (ppm)': smoke,
                             'light (lumens)' : light_received,
                             'flame (y/n)' : flame_received})


        time.sleep(5)
        
main()




