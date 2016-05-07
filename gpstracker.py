#
# GPS Tracking
#

from gps3 import GPSDSocket, Fix

import threading

gpsd = None
gps_fix = None

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = GPSDSocket("127.0.0.1")
    self.current_value = None
    self.running = True #setting the thread running to true
  def __print(self, str):
    if self.verbose:
      print ( str)

  def run(self):
    global gpsd
    global gps_fix
    gps_fix = Fix()

    for new_data in gpsd:
            self.__print("Got data")
            if new_data:
                self.__print("Refresh data")
                gps_fix.refresh(new_data)
    while self.running:
      self.__print("Gpsd next")
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer


class GpsTracker:

    def __init__(self, brainz=None, verbose=False):
        self.verbose = verbose
        self.brainz = brainz
        self.started = False
        self.latitude = 60 
        self.longitude = 20
        self.speed = 10
        self.track = 20

    def __print(self, str):
        if self.verbose:
            print ( str)

    def start(self):
        self.started = True
        # Listen on port 2947 (gpsd) of localhost
        self.gpsp = GpsPoller() # create the thread


    def stop(self):
        pass

    def tick(self,interval):
        if not self.started:
# Test values
            self.latitude = self.latitude + 0.0001;
            self.longitude = self.longitude + 0.0001;
            self.track = self.track + 2;
            return
        if (gps_fix == None):
            self.__print("No fix")
            return
        self.__print(gps_fix)
        self.speed = gps_fix.speed
        self.latitude = gps_fix.latitude
        self.longitude = gps_fix.longitude
        self.track = gps_fix.track
