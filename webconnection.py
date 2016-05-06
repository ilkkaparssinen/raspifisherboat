#
# WebConnection via web sockets
#
import time
import os
import subprocess
import datetime
import pickle
import websocket
import os.path
import json
import base64
import threading
from threading import Timer


class WebConnection:
    def __init__(self, brainz=None, verbose=False):
        self.brainz = brainz
        self.verbose = verbose
        self.ticks = 0
        self.started = False
        self.connected = False
        self.ws = None
        self.wst = None
        self.topic = "TEST"
        self.lock = threading.Lock()

    def __print(self, str):
        if self.verbose:
            print (str)

    def on_message(self, ws, message):
        self.__print("Message received")
        imess = json.loads(message)
        self.__print(imess)
        if imess["action"] == "PING":
            self.__print("ping")
        elif imess["action"] == "SETTINGS":
            self.set_settings(imess)
        else:
            self.__print("Unknown message")

    def on_error(self, ws, error):
        self.__print(error)

    def on_close(self, ws):
        self.connected = False
        self.__print("Websocket closed, Trying to reconnect")
        self.reconnect()

    def on_open(self, ws):
        self.connected = True
        self.subscribe()
        self.send_settings()
        self.__print("Websocket opened")
        self.send_message("Ahoy! Boat is ready!")

    def start(self):
        self.reconnect()
        self.started = True

    def connect(self):
        self.ws = websocket.WebSocketApp("ws://52.51.75.200:8080",
                                on_message = self.on_message,
                                on_error = self.on_error,
                                on_close = self.on_close)
        self.ws.on_open = self.on_open
        self.__print("Websocket started")
        self.wst = threading.Thread(target=self.ws.run_forever)
        self.wst.daemon = True
        self.wst.start()

    def reconnect(self):
        self.__print("Websocket  reconnect")
        if self.connected:
            return
        self.connect()

    # Just to test connection
    def tick(self,tick_time):
        if not self.started:
            return
        self.ticks = self.ticks + 1
        if self.ticks > 100:
            self.reconnect()
            self.ticks = 0

    def stop(self):
        if not self.started:
            return

    def ping(self):
        self.__print("Ping")
        mess = {}
        mess["action"] = "ping"
        self.ws.send(json.dump(mess))

    def subscribe(self):
        if not self.connected:
            return

        self.__print("Send subscribe")
        mess = {}
        mess["action"]             = "SUBSCRIBE"
        mess["topic"]              = self.topic
        mess["type"]              = "BOAT"
        self.lock.acquire()
        self.ws.send(json.dumps(mess))
        self.lock.release()

    def send_message(self,message):
        if not self.connected:
            return
        self.__print("Send chat")
        mess = {}
        mess["action"]             = "MESSAGE"
        mess["topic"]              = self.topic
        mess["who"]                = "BOAT"
        mess["message"]            = message
        self.lock.acquire()
        self.ws.send(json.dumps(mess))
        self.lock.release()


    def set_settings(self,mess):
        self.__print("Set settings!!")
        self.brainz.speed                     = mess["speed"]
        self.brainz.turn                      = mess["turn"]
        self.brainz.speed_change_cycle        = mess["speed_change_cycle"]
        self.__print("Setting")
        self.brainz.speed_motors_full_percent = mess["speed_motors_full_percent"]
        self.brainz.low_speed_percent         = mess["low_speed_percent"]
        self.brainz.play_music                = mess["play_music"]

        self.__print("Music")
        self.__print(self.brainz.play_music)
        self.__print("Speed")
        self.__print(self.brainz.speed)
        self.__print("Turn")
        self.__print(self.brainz.turn)
    def send_settings(self):
        self.__print("Send settings")
        if not self.started:
            return
        mess = {}
        mess["action"]             = "SETTINGS"
        mess["topic"]              = self.topic
        mess["speed"]              = self.brainz.speed
        mess["turn"]               = self.brainz.turn
        mess["speed_change_cycle"] = self.brainz.speed_change_cycle
        mess["speed_motors_full_percent"] = self.brainz.speed_motors_full_percent
        mess["low_speed_percent"]  = self.brainz.low_speed_percent
        mess["play_music"]         = self.brainz.play_music
        self.lock.acquire()
        xx = json.dumps(mess)
#       self.ws.send(json.dumps(mess))
        self.lock.release()
        self.__print("Sended settings")

    def send_image(self,image):
        if not self.connected:
            return
        mess = {}
        mess["action"]             = "IMAGE"
        mess["topic"]              = self.topic
        mess["image"]              = base64.b64encode(image)
#       self.__print(mess["image"])
        self.lock.acquire()
        self.ws.send(json.dumps(mess))
        self.lock.release()

    def send_status(self):
        self.__print("Send status")
        if not self.connected:
            return
        mess = {}
        mess["action"] = "STATUS"
        mess["topic"]              = self.topic
        mess["latitude"] = self.brainz.gps_tracker.latitude
        mess["longitude"] = self.brainz.gps_tracker.longitude
        mess["speed"] = self.brainz.gps_tracker.speed
        mess["track"] = self.brainz.gps_tracker.track
        mess["song"] = self.brainz.player.current_song
        mess["state"] = self.brainz.state
        mess["flex"] = self.brainz.adc_sensors.flex

        self.lock.acquire()
        self.ws.send(json.dumps(mess))
        self.lock.release()
        self.__print("sended status")
#        self.send_message("Boat speed is:" + str( self.brainz.gps_tracker.speed) + " rod bend:" + str(mess["flex"]))
