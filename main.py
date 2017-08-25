#!/usr/bin/env python

import argparse
import os
import logging
import sys
import yaml
import time

# Extend path to enable 'svvlogger' module
sys.path.append(os.path.realpath(__file__))

import svvlogger


logfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "svv_logger.log")
log = logging.getLogger("svvlogger")

log.setLevel(logging.DEBUG)
fh = logging.FileHandler(logfile)
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(logging.INFO)

log.addHandler(fh)
log.addHandler(ch)

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", default="config.yml", help="Configuration file")
parser.add_argument("-p", "--port", help="serial port to Adafruit BNO055 accelerometer", default="/dev/serial0")
parser.add_argument("-o", "--output", help="""output file for timeseries data. \
NOTE: A datetime will be added to each file to track records over multiple days.""", default="data/output")
parser.add_argument("-s", "--slack_url", help="Slack webhook url for notifications")
parser.add_argument("-d", "--db_path", help="Path to sqlite3 database file (will be created if missing)")


class TelemetryLogger:
    """
    Continously collect sensor metrics for SVV and store.
    Currently polls for GPS and accelerometer data
    """
    def __init__(self, output, serial_port, rts=18):
        self._output = output
        self._serial_port = serial_port
        self.gps_poller = svvlogger.GpsPoller()
        self.accelerometer = svvlogger.Accelerometer(serial_port, rts)

    def start(self):
        # kick off polling of gpsd data
        self.gps_poller.start()

        while True:
            time.sleep(0.5)
            gps = self.gps_poller.data()
            x, y, z = self.accelerometer.linear_acceleration()
            accel = {"x": x, "y": y, "z": z}
            log.debug("Acceleration: {}".format(accel))
            log.debug("GPS (lat: {}, lon: {}). UTC: {}".format(
                gps.fix.lat, gps.fix.lon, gps.utc))



if __name__ == '__main__':
    args = parser.parse_args()

    config_file = args.config
    cfg = {}
    if os.path.exists(config_file):
        log.info("Reading conf file found.. '{}'".format(config_file))

        with open(config_file, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

    serial_port = cfg.get("port", args.port)
    output_file = cfg.get("output", args.output)
    slack_url = cfg.get("slack_webhook_url", args.slack_url)
    db_path = cfg.get("db_path", args.db_path)

    telemetry = TelemetryLogger(output_file, serial_port)
    telemetry.start()
