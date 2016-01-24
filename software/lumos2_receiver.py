# main.py -- put your code here!
#########################
#        Imports        #
#########################


from pyb import UART, LED, Pin, Switch
from time import sleep
import sys


#########################
#     Prerequisites     #
#########################


#set up transceiver to receive data to from cansat
x3_pin = Pin('X3', Pin.OUT_PP)
x3_pin.high()

#create transceiver object on UART4
hc12 = UART(4, 9600)

#feedback-pyboard on and working
green = LED(2)
green.on()

#feedback-waiting for user to press button
orange = LED(3)
orange.on()


#########################
#      Sub Programs     #
#########################


def start():
	hc12.write('1')
	orange.off()

#create switch object
big_red_button = Switch()
big_red_button.callback(start)

finished = False
 

#########################
#       Main Loop       #
#########################
 
while finished == False: #While loop that loops forever

	if hc12.any(): 
		data = hc12.readline()
		data = data.decode('utf-8')

		dataArray = data.split(',')   #Split it into an array called dataArray

		if dataArray[0] == 'end':
			green.off()
			sleep(0.5)
			green.on()
			sleep(0.5)
			green.off()
			finished == True
		elif len(dataArray) == 6:
			tagx = dataArray[0]
			temp = dataArray[1]
			pres = dataArray[2]
			alti = dataArray[3]
			lati = dataArray[4]
			loni = dataArray[5]

		#data to analyse later
			#print('TAGX:{}'.format(tagx))
			data = str(temp) + ',' + str(pres) + ',' + str(tagx)
			print(data)
			#print('PRES:{}'.format(pres))
			#print('ALTI:{}'.format(alti))
			#print('LATI:{}'.format(lati))
			#print('LONI:{}'.format(loni))
