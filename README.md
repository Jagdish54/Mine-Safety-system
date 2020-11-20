# Mine-Safety-system
Mine safety system using Raspberry Pi, AWS Dynamodb, NRF24L01+, MQ2 , DHT22, LDR, and Flame sensors
Refer to my blog for more details.

A lot of ideas for coding taken from:
  For AWS connection: https://electronicsinnovation.com/how-to-get-raspberry-pi-to-interact-with-amazon-web-services-push-data-into-the-dynamodb/
  For NRF24L01+: https://tmrh20.blogspot.com/2019/05/automationiot-with-nrf24l01-and-mqtt.html
  For MQ2 sensor: https://tutorials-raspberrypi.com/configure-and-read-out-the-raspberry-pi-gas-sensor-mq-x/

Codes for Slave Node:
 MCP3008.py, read_Sensor_CSV_save.py, read_csv_send_master.py, read_csv_graph_generate.py.

Code for Master Node: master_nrf_aws.py

Before running any code create a blank csv file on both master and slave device. Refer to the file create_blank_csv.py.
For master device change the file name from 'node1_data.csv' to 'received_value_numbers.csv' if you're running my code.


Run the codes for slave first and then the master node.
  1. read_Sensor_CSV_save.py   2.read_csv_send_master.py  3.read_csv_graph_generate.py  4.master_nrf_aws.py

Any feedback to improve the code will be highly appreciated.
If you need to understand any part of the code write in comments either here or on my blog, happy to help.
