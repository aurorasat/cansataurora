#########################
#        Imports        #
#########################


import serial 
import matplotlib.pyplot as plt 
from drawnow import *


#########################
#     Prerequisites     #
#########################
 

tempC= []
pressure=[]
raw = serial.Serial('/dev/tty.usbmodem1412', 9600) 
plt.ion() #Tell matplotlib you want interactive mode to plot live data
cnt=0


#########################
#      Sub Programs     #
#########################
 

def makeFig(): 
    plt.ylim(0,40)
    plt.xlabel('Time (s)')
    plt.grid(True)
    plt.ylabel('Temp C')
    plt.plot(tempC, 'ro-', label='Degrees C')
    plt.legend(loc='upper left')
    plt2=plt.twinx()
    plt.ylim(98000,106000)
    plt2.plot(pressure, 'b^-', label='Pressure (Pa)')
    plt2.set_ylabel('Pressrue (Pa)')
    plt2.ticklabel_format(useOffset=False)
    plt2.legend(loc='upper right')


#########################
#       Main Loop       #
#########################
    
 
while True:
    while (raw.inWaiting()==0):
        pass
    data = raw.readline() 
    dataArray = data.split(',')
    temp = float( dataArray[0])
    P =    float( dataArray[1])
    tempC.append(temp)
    pressure.append(P)
    drawnow(makeFig)
    plt.pause(.000001)
    cnt=cnt+1
    if(cnt>=55):
        plt.ioff()
        plt.show()
        break
