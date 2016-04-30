#
# Brainz. Here's all the mushy fisherbot logic
#
# Sensors, adapters and modules that are commanded by brainz:
#
# GPS - class which handles the GPS input
# AdcSensors - ADC sensors - now only flex sensor to detect if we have fish or not
# ServerConnection - handle connection to websocket server
# Motors - handle motors by skid steering


from player import Player
from adcsensors import AdcSensors
from motors import Motors
from webconnection import WebConnection
from gpstracker import GpsTracker
from video import Video

import time
import os
import datetime
import sys
class Brainz:
    STATE_WAITING = 0
    STATE_FISHING = 1
    STATE_HASFISH = 2
    TICK_INTERVAL = 0.2
    FLEX_FISH_LIMIT = 450
    STATUS_REPORT_TICKS = 10

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.status_counter = 0
        self.state   = self.STATE_WAITING
        self.currenttime    = 0
        self.flex_fish_limit = self.FLEX_FISH_LIMIT
        self.player = Player(self,verbose)
        self.adc_sensors = AdcSensors(self,verbose)
        self.motors = Motors(self,verbose)
        self.web_connection = WebConnection(self,verbose)
        self.gps_tracker = GpsTracker(self,verbose)
        self.video = Video(self,verbose)


# Initial valus for settings
# Speed: (0-1). 1 = Full speed ahead
# Turn = -1 - +1  = +1 Only left motor on (turn to right)
#                    0 Both motors same speed
#                   -1 Only right motor on (turn to left)
        self.speed      = 0.5
        self.turn       = 0.0
# speed style examples:
#   - Constant speed = (low_speed_percent = 100)
#   - Stop and go jigging with 6 sec motor on and 4 sec stop. low_speed_percent = 0,speed_change_cycle = 10, speed_motors_full_percent = 60
#   - Trolling with 10 sec half speed and 5 sec full speed. low_speed_percent = 50, speed_change_cycle = 15, speed_motors_full_percent = 66.66
        self.speed_change_cycle = 0
        self.speed_motors_full_percent = 100
        self.low_speed_percent    = 0

# Play music or not
        self.play_music = False

    def __print(self, str):
        if self.verbose:
            print (str)


    def start(self):
        # If you dont want/have some module - just remove start method
        self.player.start()
#       self.motors.start()
#       self.adc_sensors.start()
        self.web_connection.start()
#       self.gps_tracker.start()
        self.__print('Brainz warming up')
        self.video.start()
        time.sleep(1)
        self.player.talk("Hello. Boat bot wants to start fishing")

        try:
            while True:
                self.tick()
        except:
            self.__print("Unexpected error 2:")
            self.__print( sys.exc_info()[0])
            raise
        finally:
            self.player.stop()
            self.web_connection.stop()
#           self.motors.stop()
            self.video.stop()
            self.adc_sensors.stop()
            self.__print('Brainz died')

    def tick(self):
        try:
            interval = self.TICK_INTERVAL
#           self.gps_tracker.tick(interval)
#           self.player.tick(interval)
#           self.adc_sensors.tick(interval)
            self.video.tick(interval)
#           self.motors.tick(interval)
#           self.web_connection.tick(interval)
            self.tick_check()
            self.status_counter += 1
        # Send status report to websocket server
            if self.status_counter > self.STATUS_REPORT_TICKS:
                self.web_connection.send_status()
                self.status_counter = 0

            time.sleep(self.TICK_INTERVAL)
        except:
            self.__print("Unexpected error 1:")
            self.__print( sys.exc_info()[0])
            raise

    def tick_check(self):
        if self.state == self.STATE_FISHING:
            self.fishing()

    def fishing(self):
        if self.adc_sensors.flex < self.flex_fish_limit:
            self.state = self.STATE_HASFISH
            self.player.talk("Hey there. I got a fish!")
