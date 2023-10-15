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

import struct

from sensirion_shdlc_driver.command import ShdlcCommand

class SPS30_StartMeasurement(ShdlcCommand):

    def __init__(self, output_format_uint16):
        super(SPS30_StartMeasurement, self).__init__(
                id=0x00,
                data=[0x01, 0x05] if output_format_uint16 else [0x01, 0x03],
                max_response_time=0.02)

    def interpret_response(self, data):
        return None

class SPS30_StopMeasurement(ShdlcCommand):

    def __init__(self):
        super(SPS30_StopMeasurement, self).__init__(
                id=0x01,
                data=[],
                max_response_time=0.02)

    def interpret_response(self, data):
        return None

class SPS30_ReadMeasuredValue(ShdlcCommand):

    def __init__(self, output_format_uint16):
        super(SPS30_ReadMeasuredValue, self).__init__(
                id=0x03,
                data=[],
                max_response_time=0.02)
        if output_format_uint16:
            self.format_str = '>HHHHHHHHHH'
        else:
            self.format_str = '>ffffffffff'

    def interpret_response(self, data):
        if len(data) == 0:
            return None
        (mc_pm1_0, mc_pm2_5, mc_pm4_0, mc_pm10,
         nc_pm0_5, nc_pm1_0, nc_pm2_5, nc_pm4_0, nc_pm10,
         typical_particle_size) = struct.unpack(self.format_str, data)
        return ((mc_pm1_0, mc_pm2_5, mc_pm4_0, mc_pm10),
                (nc_pm0_5, nc_pm1_0, nc_pm2_5, nc_pm4_0, nc_pm10),
                typical_particle_size)

class SPS30_Sleep(ShdlcCommand):

    def __init__(self):
        super(SPS30_Sleep, self).__init__(
                id=0x10,
                data=[],
                max_response_time=0.005)

    def interpret_response(self, data):
        return None

class SPS30_WakeUp(ShdlcCommand):

    def __init__(self):
        super(SPS30_WakeUp, self).__init__(
                id=0x11,
                data=[],
                max_response_time=0.005)

    def interpret_response(self, data):
        return None

class SPS30_StartFanCleaning(ShdlcCommand):

    def __init__(self):
        super(SPS30_StartFanCleaning, self).__init__(
                id=0x56,
                data=[],
                max_response_time=0.02)

    def interpret_response(self, data):
        return None

class SPS30_ReadAutoCleaningInterval(ShdlcCommand):

    def __init__(self):
        super(SPS30_ReadAutoCleaningInterval, self).__init__(
                id=0x80,
                data=[0x00],
                max_response_time=0.02)

    def interpret_response(self, data):
        interval_in_seconds, = struct.unpack('>I', data)
        return interval_in_seconds

class SPS30_WriteAutoCleaningInterval(ShdlcCommand):

    def __init__(self, interval_in_seconds):
        super(SPS30_WriteAutoCleaningInterval, self).__init__(
                id=0x80,
                data=b'\x00' + struct.pack('>I', interval_in_seconds),
                max_response_time=0.02)

    def interpret_response(self, data):
        return None

class SPS30_DeviceInformation(ShdlcCommand):

    def __init__(self, product_type):
        super(SPS30_DeviceInformation, self).__init__(
                id=0xD0,
                data=[0x00 if product_type else 0x03],
                max_response_time=0.02)

    def interpret_response(self, data):
        return data[:-1].decode('ascii')

class SPS30_DeviceInformation_ProductType(SPS30_DeviceInformation):

    def __init__(self):
        super(SPS30_DeviceInformation_ProductType, 
                self).__init__(product_type=True)

class SPS30_DeviceInformation_SerialNumber(SPS30_DeviceInformation):

    def __init__(self):
        super(SPS30_DeviceInformation_SerialNumber, 
                self).__init__(product_type=False)

class SPS30_ReadVersion(ShdlcCommand):

    def __init__(self):
        super(SPS30_ReadVersion, self).__init__(
                id=0xD1,
                data=[],
                max_response_time=0.02)

    def interpret_response(self, data):
        (firmware_major_version, 
                firmware_minor_version, 
                _,
                hardware_revision,
                _,
                shdlc_protocol_major_version,
                shdlc_protocol_minor_version) = struct.unpack('>BBBBBBB', data)
        return ((firmware_major_version, firmware_minor_version),
                hardware_revision,
                (shdlc_protocol_major_version, shdlc_protocol_minor_version))

class SPS30_ReadDeviceStatusRegister(ShdlcCommand):

    def __init__(self, clear_bits=False):
        super(SPS30_ReadDeviceStatusRegister, self).__init__(
                id=0xD2,
                data=[0x01 if clear_bits else 0x00],
                max_response_time=0.02)

    def interpret_response(self, data):
        (device_status_register, _) = struct.unpack('>IB', data)
        speed_warning = ((device_status_register & (1<<21)) != 0)
        laser_error = ((device_status_register & (1<<5)) != 0)
        fan_error = ((device_status_register & (1<<4)) != 0)
        return (speed_warning, laser_error, fan_error)

class SPS30_DeviceReset(ShdlcCommand):

    def __init__(self):
        super(SPS30_DeviceReset, self).__init__(
                id=0xD3,
                data=[],
                max_response_time=0.02)

    def interpret_response(self, data):
        return None
