# shdlc-sps30: SHDLC Driver for Sensirion SPS30 Kit
# Copyright (C) 2023 Mete Balci
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .commands import *
from .errors import *

from sensirion_shdlc_driver import ShdlcDeviceBase

class Sps30ShdlcDevice(ShdlcDeviceBase):

    def __init__(self, connection, slave_address=0, output_format_uint16=False):
        super(Sps30ShdlcDevice, self).__init__(connection, slave_address)
        self.output_format_uint16 = output_format_uint16
        self._register_device_errors([
            SPS30_WrongDataLengthError(),
            SPS30_UnknownCommandError(),
            SPS30_NoAccessRightForCommandError(),
            SPS30_IllegalParameterError(),
            SPS30_ArgumentOutOfRangeError(),
            SPS30_NotAllowedInCurrentStateError()])

    def get_product_type(self, as_int=False):
        product_type = self.device_information_product_type().encode('ascii')
        if as_int:
            return int(product_type, 16)
        else:
            return product_type

    def get_product_subtype(self):
        return None

    def get_article_code(self):
        return None

    def get_serial_number(self):
        return device_information_serial_number()

    # not supported, use read device status register command instead
    def get_error_state(self, clear=True, as_exception=False):
        pass

    def get_slave_address(self):
        # always 0
        return 0

    # not possible to change the slave address
    def set_slave_address(self, slave_address, update_driver=True):
        pass

    def get_baudrate(self):
        # always 115200
        return 115200

    # not possible to change the baudrate
    def set_baudrate(self):
        pass

    # 200 us is default
    def get_reply_delay(self):
        return 200

    # not supported
    def get_system_up_time(self):
        return 0

    # after calling reset, wait ~0.1 seconds
    def device_reset(self):
        return self.execute(SPS30_DeviceReset())

    # not possible to factory reset
    def factory_reset(self):
        pass 

    # not possible to change the reply delay
    def set_reply_delay():
        pass

    def get_version(self):
        ((fw_major, fw_minor), rev, (shdlc_major, shdlc_minor)) = self.read_version()
        return sensirion_shdlc_driver.types.Version(
                sensirion_shdlc_driver.types.FirmwareVersion(fw_major, fw_minor, False),
                sensirion_shdlc_driver.types.HardwareVersion(rev, 0),
                sensirion_shdlc_driver.types.ProtocolVersion(shdlc_major, shdlc_minor))

    # returns None
    def start_measurement(self):
        return self.execute(SPS30_StartMeasurement(self.output_format_uint16))

    # returns None
    def stop_measurement(self):
        return self.execute(SPS30_StopMeasurement())

    # returns tuple (
    #                (mass concentration pm1.0, pm2.5, pm4.0, pm10)
    #                (number concentration pm0.5, pm1.0, pm2.5, pm4.0, pm10)
    #                typical_particle_size 
    #               )
    # all are in output format type, either uint16 or float
    # or None
    def read_measured_value(self):
        return self.execute(SPS30_ReadMeasuredValue(self.output_format_uint16))

    # returns None
    def sleep(self):
        return self.execute(SPS30_Sleep())

    # returns None
    def wakeup(self):
        return self.execute(SPS30_WakeUp())

    # returns None
    def start_fan_cleaning(self):
        return self.execute(SPS30_StartFanCleaning())

    # returns uint32 interval in seconds
    def read_auto_cleaning_interval(self):
        return self.execute(SPS30_ReadAutoCleaningInterval())

    # returns None
    def write_auto_cleaning_interval(self, interval_in_seconds):
        return self.execute(SPS30_WriteAutoCleaningInterval(interval_in_seconds))

    # returns ascii string
    def device_information_product_type(self):
        return self.execute(SPS30_DeviceInformation_ProductType())

    # returns ascii string
    def device_information_serial_number(self):
        return self.execute(SPS30_DeviceInformation_SerialNumber())

    # returns tuple ( 
    #                (firmware major, firmware minor), 
    #                hardware revision, 
    #                (sdhlc major, sdhlc minor)
    #               )
    # all are uint8
    def read_version(self):
        return self.execute(SPS30_ReadVersion())

    # returns tuple (speed_warning, laser_error, fan_error)
    # all are bool
    def read_device_status_register(self, clear_bits):
        return self.execute(SPS30_ReadDeviceStatusRegister(clear_bits))
