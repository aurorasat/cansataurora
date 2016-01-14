# main.py -- put your code here!
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
bmp180 = BMP180('X')
bmp180.oversample_sett = 3 #0=low accuracy, 3=high accuracy
bmp180.baseline = 101325 #pressure at main sea level

#set up transceiver to send data to ground station
x3_pin = Pin('X3', Pin.OUT_PP)
x3_pin.high()

#create transceiver object on UART4
hc12 = UART(4, 9600)

#feedback-pyboard on and working
green = LED(2)
green.on()
blue = LED(4)
orange = LED(3)

finished = False


#########################
#       Main Loop       #
#########################


while finished == False:

	#if start command is received
	if hc12.any():
		orange.off()

		for i in range(0,2):
			blue.toggle()
			sleep(0.2)
			blue.toggle()
			sleep(0.2)

		#50s loop, get data every half second and write to backup.csv, and also transmit to ground station
		for tag in range(1,11):
			
			temp = bmp180.temperature
			pres = bmp180.pressure
			alt = bmp180.altitude
			location = 0

			#open backup.csv to write data to, write to it, then close it
			backup = open('/sd/backup.csv', 'a')
			backup.write('{},{},{},{},{}\n'.format(tag,temp,pres,alt,location))
			backup.close()

			data = str(tag) + ',' + str(temp) + ',' + str(pres) + ',' + str(alt) + ',' + str(location) #concatenate data with commas

			hc12.write(data) #write data over UART4 to transmit to ground station

			sleep(1) #sleep for a second to buffer

		finished = True

	else:
		orange.on()


#########################
#      End Program      #
#########################


for i in range(0,4):
	green.toggle()
	sleep(0.2)
	green.toggle()
	sleep(0.2)
	
green.off()