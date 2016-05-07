#
# GPS Tracking
#
import gps
import threading

# Listen on port 2947 (gpsd) of localhost


class GpsTracker:
    def __init__(self, brainz=None, verbose=False):
        self.verbose = verbose
        self.brainz = brainz
        self.started = False
        self.latitude = 60
        self.longitude = 20
        self.speed = 10
        self.track = 20
        self.session = None
        self.read_thread = None

    def __print(self, str):
        if self.verbose:
            print (str)

    def connect(self):
        self.__print("Connect")
        self.session = gps.gps("127.0.0.1", "2947")
        self.session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
        # Listen on port 2947 (gpsd) of localhost
        self.__print("Start thread")
        self.read_thread = threading.Thread(target=self.poll)
        self.read_thread.daemon = True
        self.read_thread.start()

    def poll(self):
        self.__print("Poll")
        while True:
            try:
                report = self.session.next()
                # Wait for a 'TPV' report and display the current time
                # To see all report data, uncomment the line below
                print report
                if report['class'] == 'TPV':
                    if hasattr(report, 'lat'):
                        self.latitude = report.lat
                    if hasattr(report, 'lon'):
                        self.longitude = report.lon
                    if hasattr(report, 'speed'):
                        self.speed = report.speed
                    if hasattr(report, 'track'):
                        self.track = report.track
            except KeyboardInterrupt:
                quit()
            except StopIteration:
                self.session = None
                print "GPSD has terminated"

    def start(self):
        self.started = True
        self.connect() 

    def stop(self):
        pass

    def tick(self, interval):
        if not self.started:
            # Test values
            self.latitude = self.latitude + 0.0001;
            self.longitude = self.longitude + 0.0001;
            self.track = self.track + 2;
            return
        if (self.session == None):
            self.__print("No fix")
            return
        # self.__print(gps_fix)
        # self.speed = gps_fix.speed
        # self.latitude = gps_fix.latitude
        # self.longitude = gps_fix.longitude
        # self.track = gps_fix.track
        
