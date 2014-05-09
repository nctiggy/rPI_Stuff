#!/usr/bin/env python

# Example for RC timing reading for Raspberry Pi
# Must be used with GPIO 0.3.1a or later - earlier verions
# are not fast enough!

import time
import RPi.GPIO as GPIO, time, os
import numpy
import urllib2
import json

DEBUG = 1
GPIO.setmode(GPIO.BCM)
url = 'http://hotwheels.cfapps.io/widgets/mph'
headers = {'Content-type': 'application/json'}


def RCtime (RCpin):
    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.005)

    GPIO.setup(RCpin, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    while (GPIO.input(RCpin) == GPIO.LOW):
        reading += 1
    return reading

calibrateA=[]
calibrateB=[]
for x in range(0, 20):
    calibrateA.append(RCtime(17))
triggerA = numpy.mean(calibrateA) * 1.75
# print triggerA                               
for x in range(0, 20):
    calibrateB.append(RCtime(18))
triggerB = numpy.mean(calibrateB) * 1.75
#print triggerB

while True:
    while RCtime(17) < triggerA:
        pass
    #print time.asctime( time.localtime(time.time()) )
    timeA = int(round(time.time() * 1000))
    while RCtime(18) < triggerB:
        pass
    #print time.asctime( time.localtime(time.time()) )
    timeB = int(round(time.time() *1000))
    totalTime =  timeB-timeA
    speedMPH = format((3600000/totalTime)/4295.59, '.2f')
    data = {"auth_token":"YOUR_AUTH_TOKEN","current":speedMPH}
    data_json = json.dumps(data)
    req = urllib2.Request(url, data=data_json, headers=headers)
    try:
        f = urllib2.urlopen(req)
    except:
        pass
    f.close()