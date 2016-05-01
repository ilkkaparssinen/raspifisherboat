#
# Internal camera, use videofeed to get hand commands
#
import time
import os
import subprocess
import datetime

import picamera
import picamera.array
import numpy as np
import threading
import io


class Video:
    def __init__(self, brainz=None, verbose=False):
        self.brainz = brainz
        self.verbose = verbose
        self.camera = None
        self.motion_detected = False
        self.i = 0
        self.wst = None
        self.started = False

    def __print(self, str):
        if self.verbose:
            print (str)

    def start(self):
        self.started = True

        self.camera = picamera.PiCamera()
        self.camera.resolution = (160, 120)
        self.camera.framerate = 5
        self.__print('Waiting 2 seconds for the camera to warm up')
        time.sleep(2)

        self.__print('Started recording')
        self.wst = threading.Thread(target=self.record_camera)
        self.wst.daemon = True
        self.wst.start()



    def record_camera(self):
        stream=io.BytesIO()

        for foo in self.camera.capture_continuous(stream,'jpeg',True):
#           img = stream.getvalue()
            self.__print("Image")
            self.brainz.web_connection.send_image(stream.getvalue())
            stream.seek(0)
            stream.truncate()

    def tick(self,interval):
        pass

    def stop(self):
        if not self.started:
            return

        self.camera.stop_recording()
        self.__print('Stopped recording')

