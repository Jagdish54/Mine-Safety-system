
#Create blank csv for slave
import csv
with open('node1_data.csv', 'w+', newline ='') as csvfile:
    fieldnames = ['timestamp',
                  'temperature (C)',
                  'humidity (%)',
                  'lpg (ppm)',
                  'carbon monoxide (ppm)',
                  'smoke (ppm)',
                  'light (lux)',
                  'flame (y/n)']

    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)

    writer.writeheader()
    

#Create a blank csv for master


#import csv
#with open('received_value_numbers.csv', 'w+', newline ='') as csvfile:
#    fieldnames = ['timestamp',
#                          'temperature (C)',
#                          'humidity (%)',
#                          'lpg (ppm)',
#                          'carbon monoxide (ppm)',
#                          'smoke (ppm)',
#                          'light (lux)',
#                          'flame (y/n)']
#                
#    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
#                
#    writer.writeheader()
