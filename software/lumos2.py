# main.py -- put your code here!
#########################
#        Imports        #
#########################


from bmp180 import BMP180
from pyb import UART, LED, Pin
from time import sleep
from micropyGPS import MicropyGPS


#########################
#     Prerequisites     #
#########################


#create BMP180 object
bmp180 = BMP180('X')
bmp180.oversample_sett = 3 #0=low accuracy, 3=high accuracy
bmp180.baseline = 101325 #pressure at main sea level

#create GPS object
my_gps = MicropyGPS()

#set up transceiver to send data to ground station
x3_pin = Pin('X3', Pin.OUT_PP)
x3_pin.high()

#create transceiver object on UART4
hc12 = UART(4, 9600)

#create gps object on UART3
uart = UART(3, 9600)

#feedback-pyboard on and working
green = LED(2)
green.on()

#feedback-received start command
blue = LED(4)

#feedback-waiting for user to press button
orange = LED(3)
orange.on()

#boolean variable to manage main loop
finished = False

#########################
#       Main Loop       #
#########################


while finished == False:
	#if start command is received
	if hc12.any():
		orange.off()

		#for local use only
		for i in range(0,2):
			blue.toggle()
			sleep(0.4)
			blue.toggle()
			sleep(0.4)

		#X second loop, get data every half second and write to backup.csv, and also transmit to ground station
		for tag in range(1,61):

			green.off()
			
			temp = bmp180.temperature
			pres = bmp180.pressure
			alt = bmp180.altitude

			#if there is gps data to be read
			while uart.any():
				my_sentence = chr(uart.readchar())

			for x in my_sentence:
				my_gps.update(x)

			latitude = my_gps.latitude_string()
			longitude = my_gps.longitude_string()
			timestamp = my_gps.timestamp
			#alt2 = my_gps.altitude

			#open backup.csv to write data to, write to it, then close it
			backup = open('/sd/backup.csv', 'a')
			backup.write('{},{},{},{},{},{},{}\n'.format(tag,timestamp,temp,pres,alt,latitude,longitude))
			backup.close()

			data = str(tag) + ',' + str(temp) + ',' + str(pres) + ',' + str(alt) + ',' + str(latitude) + ',' + str(longitude) #concatenate data with commas

			hc12.write(data) #write data over UART4 to transmit to ground station

			green.on()
			sleep(1) #sleep for a second to buffer

		finished = True
		sleep(2)
		hc12.write('end')


#########################
#      End Program      #
#########################


for i in range(0,4):
	blue.toggle()
	sleep(0.2)
	blue.toggle()
	sleep(0.2)
	
green.off()
blue.off()
