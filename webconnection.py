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

class WebConnection:
    def __init__(self, brainz=None, verbose=False):
        self.brainz = brainz
        self.verbose = verbose
        self.ticks = 0
        self.started = False
        self.ws = None

    def __print(self, str):
        if self.verbose:
            print (str)

    def on_message(self, ws, message):
        self.__print(message)
        imess = json.loads(message)
        if imess.action == "ping":
            self.__print("ping")
        elif imess.action == "set":
            self.set_settings(imess)
        else:
            self.__print("Unknown message")

    def on_error(self, ws, error):
        self.print(error)

    def on_close(self, ws):
        pass

    def on_open(self, ws):
        ws.send("Hello %d" % i)

    def start(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("ws://127.0.0.1:80/foo",
                                on_message = self.on_message,
                                on_error = self.on_error,
                                on_close = self.on_close)

        self.started = True

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

    def set_settings(self,mess):
        self.brainz.speed                     = mess["speed"]
        self.brainz.turn                      = mess["turn"]
        self.brainz.speed_change_cycle        = mess["speed_change_cycle"]
        self.brainz.speed_motors_full_percent = mess["speed_motors_full_percent"]
        self.brainz.speed_change_percent      = mess["speed_change_percent"]
        self.brainz.play_music                = mess["play_music"]

    def send_status(self):
        if not self.started:
            return
        mess = {}
        mess["action"] = "status"
        mess["latitude"] = self.brainz.gps_tracker.latitude
        mess["longitude"] = self.brainz.gps_tracker.longitude
        mess["speed"] = self.brainz.gps_tracker.speed
        mess["track"] = self.brainz.gps_tracker.track
        mess["song"] = self.brainz.player.current_song
        mess["state"] = self.brainz.state

        self.ws.send(json.dump(mess))
