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

  def run(self):
    global gpsd
    global gps_fix
    gps_fix = Fix()

    for new_data in gpsd:
            if new_data:
                gps_fix.refresh(new_data)
    while self.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer


class GpsTracker:

    def __init__(self, brainz=None, verbose=False):
        self.verbose = verbose
        self.brainz = brainz
        self.started = False
        self.latitude = 0
        self.longitude = 0
        self.speed = 0
        self.track = 0

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
            return

        self.__print(gps_fix)
        self.speed = gps_fix.speed
        self.latitude = gps_fix.latitude
        self.longitude = gps_fix.longitude
        self.track = gps_fix.track
