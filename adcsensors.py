# Flex sensor - detect fish + temperature sensor. Default - use channel 0
#
import time
import os
import subprocess
import datetime
import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Flex sensor connected to adc #0

FLEXSENSOR_ADC=0

# set up the SPI interface pins

import spidev
import time
import os



class AdcSensors:
    def __init__(self, brainz=None, verbose=False):
        self.verbose = verbose
        self.brainz = brainz
        self.started = False
        self.flex = 0

    def __print(self, str):
        if self.verbose:
            print ( str)

    def start(self):
        self.started = True
        self.__print("Starting adc sensors")
        # Open SPI bus
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)

    def stop(self):
        pass

    def read_sensor(self):
        pass


# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7

    def readADC(self,channel):
        adc = self.spi.xfer2([1,(8 + channel) << 4,0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data


    def tick(self,tick_time):
        if not self.started:
            return
        self.flex = self.readADC(FLEXSENSOR_ADC)


