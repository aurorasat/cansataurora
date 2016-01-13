#########################
#        Imports        #
#########################


from pyb import UART, LED, Pin
from time import sleep
import matplotlib.pyplot as plt
from drawnow import *


#########################
#     Prerequisites     #
#########################


#set up transceiver to receive data to from cansat
x3_pin = Pin('X3', Pin.OUT_PP)
x3_pin.high()

#create transceiver object on UART4
hc12 = UART(4, 9600)

#feedback-pyboard on and working
LED(4).on

#data to analyse later
log = open('/sd/log.csv', 'w')
 
temperature= []
pressure=[]
plt.ion() #Tell matplotlib you want interactive mode to plot live data
counter=0


#########################
#      Sub Programs     #
#########################
 

def makeFig(): #Create a function that makes our desired plot
    plt.ylim(0,50)                                 #Set y min and max values
    plt.title('Primary Mission')      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('Temp C')                            #Set ylabels
    plt.plot(tempF, 'ro-', label='Degrees C')       #plot the temperature
    plt.legend(loc='upper left')                    #plot the legend
    plt2=plt.twinx()                                #Create a second y axis
    plt.ylim(10000,11000)                           #Set limits of second y axis- adjust to readings you are getting
    plt2.plot(pressure, 'b^-', label='Pressure (Pa)') #plot pressure data
    plt2.set_ylabel('Pressrue (Pa)')                    #label second y axis
    plt2.ticklabel_format(useOffset=False)           #Force matplotlib to NOT autoscale y axis
    plt2.legend(loc='upper right')                  #plot the legend


#########################
#       Main Loop       #
#########################

start = raw_input("Begin?: ")
    
 
while True: # While loop that loops forever
	if hc12.any():
		data = hc12.readline()
		data = data.decode('utf-8')
		dataArray = data.split(',')   #Split it into an array called dataArray
		tag = float(dataArray[0])            #Convert first element to floating number and put in temp
		temp = float(dataArray[1])            #Convert second element to floating number and put in P
		pres = float(dataArray[2])
		alt = float(dataArray[3])
		location = float(dataArray[4])

		log.write('{},{},{},{},{}\n'.format(tag,temp,pres,alt,location))

		temperature.append(temp)                     #Build our tempF array by appending temp readings
		pressure.append(pres)                     #Building our pressure array by appending P readings
		altitude.append(alt) 
		drawnow(makeFig)                       #Call drawnow to update our live graph
		plt.pause(.00001)                     #Pause Briefly. Important to keep drawnow from crashing
		counter+=1
		#if(counter>50):                            #If you have 50 or more points, delete the first one from the array
			#tempF.pop(0)                       #This allows us to just see the last 50 data points
			#pressure.pop(0)


#########################
#      End Program      #
#########################


backup.close()
LED(4).off
