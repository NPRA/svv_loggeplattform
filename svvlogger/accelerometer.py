import sys
from Adafruit_BNO055 import BNO055
import logging
import time

log = logging.getLogger("svvlogger")


class Accelerometer:
    """
    Encapsulation of the BNO055 python package from Adafruit.
    """

    def __init__(self, serial_port, rts):
        self._serial_port = serial_port
        self._rts = 18
        self._started = False

        try:
            self._bno = BNO055.BNO055(serial_port=self._serial_port, rts=self._rts)
        except Exception:
            log.exception("Unable to construct BNO055 object!")
            return

        for i in range(3):
            try:
                if self._bno.begin():
                    self._started = True
                    log.debug("BNO055 successfully initialized!")
                    break
                else:
                    log.warn("BNO055 not properly responding. Retry.")
                    time.sleep(1)
            except Exception as e:
                log.warn("Issues trying to initialize BNO055: {}".format(e))
                continue

        if not self._started:
            log.error("Unable to initilize BNO055..")
            sys.exit(1)

        status, self_test, err = self.status()
        if status == 0x01:
            log.error('System error: {0}'.format(err))
            log.error('See datasheet section 4.3.59 for the meaning.')
            sys.exit(1)

    def status(self):
        system_status = self._bno.get_system_status()
        return system_status

    def revision(self):
        system_revision = self._bno.get_revision()
        return system_revision

    def calibrate(self):
        if not self._started:
            log.warn("BNO055 not started yet.")
            return

        # special calibration sequence
        self._bno.set_calibration(
            [246, 255, 176, 255, 10, 0, 163, 2, 119, 1, 214, 0,
                254, 255, 253, 255, 1, 0, 232, 3, 40, 3])

    def calibration_status(self):
        return self._bno.get_calibration_status()

    @property
    def euler(self):
        return self._bno.read_euler()

    @property
    def linear_acceleration(self):
        return self._bno.read_linear_acceleration()

    def __repr__(self):
        return "{}(started={})".format(self.__class__.__name__,
                                       self._started)
