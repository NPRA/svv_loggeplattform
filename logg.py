import logging
import sys
from datetime import datetime
import os
from gps import *
from time import *
import time
import threading
from Adafruit_BNO055 import BNO055

logging.basicConfig(filename='info_om_sensor.log', level=logging.DEBUG)
log = logging.getLogger("svvlogger")


def createfilename():
    base = "/home/pi/telemetri/data/gps_"
    timestr = time.strftime("%Y%m%d-%H%M%S")
    suffix = ".txt"

    filename = os.path.join(base, timestr, suffix)
    log.info("Creating {}".format(filename))

    return filename


def write_row(file, gpsd, observation_number, acceleration):
    fmt = "{};{g.utc};{g.fix.lat};{g.fix.lon};{g.fix.speed};{c[x]};{c[y]};{c[z]};\n"
    file.write(fmt.format(observation_number, g=gpsd, c=acceleration))
    # file.write(str(observation_number) + ';')
    # file.write(gpsd.utc +';')
    # file.write(str(gpsd.fix.latitude) +';')
    # file.write(str(gpsd.fix.longitude) +';')
    # file.write(str(gpsd.fix.speed) +';')
    # file.write(str(x) +';')
    # file.write(str(y) +';')
    # file.write(str(z) +';')
    # file.write('\n')


class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd #bring it in scope
        gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
        self.current_value = None
        self.running = True #setting the thread running to true

    def run(self):
        global gpsd
        while gpsp.running:
            gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

if __name__ == '__main__':
    observation_number = 0
    gpsfile = open(createfilename(),'w')
    gpsfile.write('id;utc;lat;lon;speed;x;y;z\n')
    gpsd = None #seting the global variable
    os.system('clear') #clear the terminal (optional)
    gpsp = GpsPoller() # create the thread
    try:
        gpsp.start() # start it up
        bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18 )
        print("Wait for accelerometer to start up")
        # Initialize the BNO055 and stop if something went wrong.
        try:
            if not bno.begin():
                raise RuntimeError('Could not start accelerometer')
        except RuntimeError:
            print("Second try to start")
            time.sleep(3)
            bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)
            time.sleep(1)
            bno.begin()


         # Print system status and self test result.
        status, self_test, error = bno.get_system_status()
        print('System status: {0}'.format(status))
        print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
        # Print out an error if system status is in error mode.

        if status == 0x01:
            print('System error: {0}'.format(error))
            print('See datasheet section 4.3.59 for the meaning.')

        # Print BNO055 software revision and other diagnostic data.
        sw, bl, accel, mag, gyro = bno.get_revision()
        print('Software version:   {0}'.format(sw))
        print('Bootloader version: {0}'.format(bl))
        print('Accelerometer ID:   0x{0:02X}'.format(accel))
        print('Magnetometer ID:    0x{0:02X}'.format(mag))
        print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

        print('Reading BNO055 data, press Ctrl-C to quit...')
        bno.set_calibration([246, 255, 176, 255, 10, 0, 163, 2, 119, 1, 214, 0, 254, 255, 253, 255, 1, 0, 232, 3, 40, 3])

        while True:
            # Read the Euler angles for heading, roll, pitch (all in degrees).
            heading, roll, pitch = bno.read_euler()
            # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
            #if not bno.begin():
            sys, gyro, accel, mag = bno.get_calibration_status()
            # Print everything out.
            print('{0} Heading={1:0.2F} Roll={2:0.2F} Pitch={3:0.2F}\tSys_cal={4} Gyro_cal={5} Accel_cal={6} Mag_cal={7}'.format(
                 str(datetime.now()),heading, roll, pitch, sys, gyro, accel, mag))
            # Other values you can optionally read:
            # Orientation as a quaternion:
            #x,y,z,w = bno.read_quaterion()
            # Sensor temperature in degrees Celsius:
            #temp_c = bno.read_temp()
            # Magnetometer data (in micro-Teslas):
            #x,y,z = bno.read_magnetometer()
            # Gyroscope data (in degrees per second):
            #x,y,z = bno.read_gyroscope()
            # Accelerometer data (in meters per second squared):
            #x,y,z = bno.read_accelerometer()
            # Linear acceleration data (i.e. acceleration from movement, not gravity--
            # returned in meters per second squared):
            x,y,z = bno.read_linear_acceleration()
            # Gravity acceleration data (i.e. acceleration just from gravity--returned
            # in meters per second squared):
            #x,y,z = bno.read_gravity()
            # Sleep for a second until the next reading.
            #print bno.get_calibration()
            observation_number += 1
            if observation_number % 10 == 0:
                #print bno.get_calibration()
                #logging.debug(bno.get_calibration())
                pass
            write_row(gpsfile, gpsd, observation_number)
            #disp.clear()
            #disp.display()
            #draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
            #draw.text((1,1), str(x), font=font)
            #draw.text((1,10), str(y), font=font)
            #draw.text((1,20), str(z), font=font)
            #disp.image(image)
            #disp.display()
            time.sleep(0.05)
    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
        print "\nKilling Thread..."
        gpsp.running = False
        gpsp.join() # wait for the thread to finish what it's doing
        gpsfile.close()
        #draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
        #disp.image(image)
        #disp.display()
    print "Done logging data.\nExiting."

