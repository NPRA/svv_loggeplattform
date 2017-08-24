import threading
import time


try:
    from gps import *
except ImportError as e:
    class gps:
        def __init__(*a, **kw):
            pass

        def next(self):
            pass

    WATCH_ENABLE = 1


class GpsPoller(threading.Thread):
    """
    Threaded class that handles the polling of GPS data
    from the "gpsd" daemon.
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.gps_daemon = gps(mode=WATCH_ENABLE)
        self.running = False

    def run(self):
        self.running = True

        while self.gps_daemon.running:
            self.gps_daemon.next()

