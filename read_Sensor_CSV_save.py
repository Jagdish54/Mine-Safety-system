#Import Library
from mq import *
import sys, time
from MCP3008 import MCP3008
import Adafruit_DHT
import time
from gpiozero import MCP3008
import RPi.GPIO as GPIO
import os
from datetime import datetime
import csv

def getMac(interface = 'eth0'):
#A statement to read and get the mac address of the ethernet interface.
    str = open('/sys/class/net/%s/address' %interface).read()
    return str[0:17]
#Create a variable named mac_id to store the mac address received from getMac() statement.
mac_id = getMac()
#define a constant for the sensor that we want to utilize for the DHT Library.
#Set the type of the sensor as DHT22.
DHT_SENSOR = Adafruit_DHT.DHT22
# Define GPIO pin that the DHT22 is plugged into on the Raspberry Pi.
DHT_PIN = 4
# Define the pin connection for buzzer into pi.
triggerPIN_buzzer = 21
#Define the GPIO pin that flame sensor is connected to the pi. 
channel_flame = 24
#Select GPIO mode as Broadcom GPIO numbers(BCM).
GPIO.setmode(GPIO.BCM)
#Set GPIO pin as an input for flame sensor.
GPIO.setup(channel_flame, GPIO.IN)
#Disable warnings
GPIO.setwarnings(False)
#Set GPIO pin as an output for buzzer.
GPIO.setup(triggerPIN_buzzer,GPIO.OUT)
#Define the frequency used for the buzzer in Hz.
buzzer = GPIO.PWM(triggerPIN_buzzer,3520 )
#Resistance of the LDR sensor.
Resistance = 10
#Define the voltage connected to LDR sensor from pi.
LDR_pi_voltage = 5
#Create a variable for the flame using intial vlaue as 0
flame = 0
#Call out the function from another python file in variable mq.
mq = MQ();
def run():
#Define a statement for reading the sensor data with error execption and in the loop. 
    try:
        while True:
#Read the sensor value of gas sensor from the function of mq.py file.
            perc = mq.MQPercentage()
#moves the text to the left side of the page.
            sys.stdout.write("\r")
#Clear to the end of line.
            sys.stdout.write("\033[K")
#Print the gas value.
            sys.stdout.write("LPG: %g ppm, CO: %g ppm, Smoke: %g ppm" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
# Format the recieved gas vlaues of lpg, CO and smoke as round of 5.           
            lpg_value = round(perc["GAS_LPG"], 5)
            co_value = round(perc["CO"], 5)
            smoke_value = round(perc["SMOKE"],5)
#flush the buffer.
            sys.stdout.flush()
#Sleep for 0.1 sec.
            time.sleep(0.1)
#Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
            humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).  
# If this happens sleep for 0.1 sec.
            if humidity is not None and temperature is not None:
#If the value is not null then print Temperature and humidity in the format of round of 2.
                print(("Temp={0:0.1f}C Humidity={1:0.1f}%".format(round(temperature, 2), round(humidity,2))))
#Create variable as humidity and temperature with format of round of 2.
                humidity = round(humidity,2)
                temperature = round(temperature, 2)
            
            else:
                time.sleep(0.1);
#Set the channel of MCP in which the LDR sensor is connected.
            LDR_MCP_PIN = MCP3008(channel=1)
#Calculate the voltage from the multiplication of the value read from channel 1
#and voltage of raspberry pi which is 3.3.
            voltage = 3.3 * LDR_MCP_PIN.value
#Calculate ADC value of the received voltage.        
            value_1 = (1023*voltage)/5
# Multiply the ADC value with LSB value which is constant.         
            value_2 = value_1*0.0048828125
#Calculate lux using the formula and format it to round of 3.
            lux0 = 500/(Resistance*((LDR_pi_voltage-value_2)/value_2))
            lux0 = round(lux0, 3)
#Print the lux value
            print("Lux = ", lux0);
            time.sleep(0.1)
#Set if statement for the value recieved.
#If the value recieved from multiple sensor justify the statement then buzzer will
#start and if not then buzzer will stop.
            if lux0 < 5 or temperature > 40 or lpg_value > 12500 or co_value > 70 or smoke_value > 51:
                buzzer.start(10)
            else:
                buzzer.stop()
#Set the if statement in which if the GPIO pin of flame sensor connected in pi
#receives data then set the flame value to 1, print the provided statement and start
#the buzzer and if not then set the flame value to 0 and print statement.
            if (GPIO.input(channel_flame)==True):
                flame = 1
                print("Flame = Yes")
                buzzer.start(10)
            else:
                flame = 0
                print("Flame = No")
#Get the current date and time
            now_time = datetime.now()
#Set the datetime format.
            timestamp_string = now_time.strftime("%m-%d-%Y %H:%M:%S")
#Open the csv file.           
            
            with open('node1_data.csv', 'a', newline ='') as csvfile:
#Create a columns 
                fieldnames = ['timestamp',
                              'temperature (C)',
                              'humidity (%)',
                              'lpg (ppm)',
                              'carbon monoxide (ppm)',
                              'smoke (ppm)',
                              'light (lux)',
                              'flame (y/n)']
#write the columns in the csv file created.
                writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
#Write the received value from the sensor to the provided columns in csv file.
                writer.writerow({'timestamp': timestamp_string,
                                 'temperature (C)' : temperature,
                                 'humidity (%)' : humidity,
                                 'lpg (ppm)': lpg_value,
                                 'carbon monoxide (ppm)': co_value,
                                 'smoke (ppm)': smoke_value,
                                 'light (lux)' : lux0,
                                 'flame (y/n)' : flame})
            time.sleep(1)            
#If there is value error print the statement and rerun the function.           
    except ValueError:
        print("Gas detected")
        run()
#For other execption returns the value of the error.
    except:
        print("Error Occurred, error code: \n", sys.exc_info())
#Clean up all the ports used.
    finally:
        GPIO.cleanup()
#Call the function.
run()
