#########################
#        Imports        #
#########################


from bmp180 import BMP180
from pyb import UART, LED, Pin, millis
from time import sleep


#########################
#     Prerequisites     #
#########################

#create BMP180 object
bmp180 = BMP180()
bmp180.oversample_sett = 3 #0=low accuracy, 3=high accuracy
bmp180.baseline = 101325 #pressure at main sea level

#set up transceiver to send data to ground station
x3_pin = Pin('X3', Pin.OUT_PP)
x3_pin.high()

#create transceiver object on UART4
hc12 = UART(4, 9600)

#feedback-pyboard on and working
LED(4).on

#open backup.csv to write data to
backup = open('/sd/backup.csv', 'w')


#########################
#       Main Loop       #
#########################


#50s loop, get data every half second and write to backup.csv, and also transmit to ground station
for tag in range(50):
	temp = bmp180.temperature
	pres = bmp180.pressure
	alt = bmp180.altitude
	backup.write('{},{},{},{},{}\n'.format(tag,temp,pres,alt,location))

	data = str(tag) + ',' + str(temp) + ',' + str(pres) + ',' + str(alt) + ',' + str(location) #concatenate data with commas
	hc12.write(data) #write data over UART4 to transmit to ground station

	sleep(1) #sleep for a second to buffer


#########################
#      End Program      #
#########################


backup.close()
LED(4).off
