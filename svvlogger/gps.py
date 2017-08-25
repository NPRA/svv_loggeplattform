import threading
import logging

log = logging.getLogger("svvlogger")

try:
    from gps import *
except ImportError as e:
    log.exception("Error importing gps package")
    log.warn("Creating a dummy gps class for testing purposes..")
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
        self.gps_data = gps(mode=WATCH_ENABLE)
        self.running = False

    def run(self):
        self.running = True

        while self.running:
            self.gps_data.next()

    def data(self):
        return self.gps_data
