#!/usr/bin/env python3

import time

from shdlc_sps30.device import Sps30ShdlcDevice

from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection
from sensirion_shdlc_driver.errors import ShdlcTimeoutError

sps30_product_type = '00080000'

def main():
    with ShdlcSerialPort(port='/dev/ttyUSB0', baudrate=115200) as port:

        device = Sps30ShdlcDevice(ShdlcConnection(port))

        device.device_reset()
        time.sleep(0.1)

        product_type = device.device_information_product_type()
        print("product_type: %s" % product_type)
        assert product_type == sps30_product_type

        serial_number = device.device_information_serial_number()
        print("serial_number: %s" % serial_number)

        ((fw_major, fw_minor), rev, (shdlc_major, shdlc_minor)) = device.read_version()
        print('fw: %d.%d rev: %d shdlc: %d.%d' % (
            fw_major, fw_minor,
            rev,
            shdlc_major, shdlc_minor))

        # default auto cleaning interval is 604800 seconds = 1 week
        device.write_auto_cleaning_interval(604800)
        auto_cleaning_interval = device.read_auto_cleaning_interval()
        print(auto_cleaning_interval)

        device_status = device.read_device_status_register(False)
        print(device_status)
        assert device_status == (False, False, False)

        # start measurement
        device.start_measurement()

        # manual fan cleaning
        # start_fan_cleaning(device)

        # read a measurement
        val = None
        # skip until a new measurement is read (not None)
        while val is None:
            val = device.read_measured_value()
            time.sleep(1)
        print(val)

        # stop measurement
        device.stop_measurement()

if __name__ == '__main__':
    main()
