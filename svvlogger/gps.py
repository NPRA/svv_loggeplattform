import threading
import logging

log = logging.getLogger("svvlogger")

try:
    #from gps import *
    from gps3py import gps
except ImportError as e:
    import sys
    log.exception("Error importing gps package")
    sys.exit(1)


class GpsPoller(threading.Thread):
    """
    Threaded class that handles the polling of GPS data
    from the "gpsd" daemon.
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.gps_data = gps.GPS(mode=gps.WATCH_ENABLE)
        self.running = False

    def run(self):
        self.running = True

        while self.running:
            self.gps_data.next()

    def data(self):
        return self.gps_data
