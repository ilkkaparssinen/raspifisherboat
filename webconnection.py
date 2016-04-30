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


class WebConnection:
    def __init__(self, brainz=None, verbose=False):
        self.brainz = brainz
        self.verbose = verbose
        self.ticks = 0
        self.started = False
        self.ws = None
        self.wst = None
        self.topic = "TEST"

    def __print(self, str):
        if self.verbose:
            print (str)

    def on_message(self, ws, message):
        self.__print(message)
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
        self.__print("Websocket closed")

    def on_open(self, ws):
        self.subscribe()
        self.started = True
        self.send_settings()
        self.__print("Websocket opened")

    def start(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("ws://52.51.75.200:8080",
                                on_message = self.on_message,
                                on_error = self.on_error,
                                on_close = self.on_close)
        self.ws.on_open = self.on_open
        self.__print("Websocket started")
        self.wst = threading.Thread(target=self.ws.run_forever)
        self.wst.daemon = True
        self.wst.start()


    # Just to test connection
    def tick(self,tick_time):
        if not self.started:
            return
        self.ticks = self.ticks + 1
        if self.ticks > 1000:
            self.ticks = 0
            self.ping()

    def stop(self):
        if not self.started:
            return

    def ping(self):
        self.__print("Ping")
        mess = {}
        mess["action"] = "ping"
        self.ws.send(json.dump(mess))

    def subscribe(self):
        self.__print("Set settings")
        mess = {}
        mess["action"]             = "SUBSCRIBE"
        mess["topic"]              = self.topic
        mess["type"]              = "BOAT"
        self.ws.send(json.dumps(mess))


    def set_settings(self,mess):
        self.__print("Set settings")
        self.brainz.speed                     = mess["speed"]
        self.brainz.turn                      = mess["turn"]
        self.brainz.speed_change_cycle        = mess["speed_change_cycle"]
        self.brainz.speed_motors_full_percent = mess["speed_motors_full_percent"]
        self.brainz.low_speed_percent         = mess["low_speed_percent"]
        self.brainz.play_music                = mess["play_music"]

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
        self.ws.send(json.dumps(mess))

    def send_image(self,image):
        self.__print("image")
        if not self.started:
            return
        mess = {}
        mess["action"]             = "VIDEO"
        mess["topic"]              = self.topic
        mess["image"]              = base64.b64decode(image)
        self.ws.send(json.dumps(mess))

    def send_status(self):
        self.__print("Send status")
        if not self.started:
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

        self.ws.send(json.dumps(mess))
