# main.py -- put your code here!
#########################
#        Imports        #
#########################


from pyb import UART, LED, Pin
import pyb
from time import sleep


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
#       Main Loop       #
#########################

first_loop = False
 
while True: #While loop that loops forever
	if first_loop == False:
		pyb.Switch().callback(lambda: hc12.write('1'))
		first_loop = True
		orange.off()
	if hc12.any():
		data = hc12.readline()
		data = data.decode('utf-8')
		dataArray = data.split(',')   #Split it into an array called dataArray

		#data to analyse later
		print(dataArray)


#########################
#      End Program      #
#########################


for i in range(0,4):
	green.toggle()
	sleep(0.2)
	green.toggle()
	sleep(0.2)
	
green.off()
