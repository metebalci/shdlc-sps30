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

from sensirion_shdlc_driver.errors import ShdlcDeviceError

class SPS30_WrongDataLengthError(ShdlcDeviceError):

    def __init__(self):
        super(SPS30_WrongDataLengthError, 
                self).__init__(0x01, 
                        "Wrong data length for this command (too much or little data)")

class SPS30_UnknownCommandError(ShdlcDeviceError):

    def __init__(self):
        super(SPS30_UnknownCommandError, 
                self).__init__(0x02, 
                        "Unknown command")

class SPS30_NoAccessRightForCommandError(ShdlcDeviceError):

    def __init__(self):
        super(SPS30_NoAccessRightForCommandError, 
                self).__init__(0x03, 
                        "No access right for command")

class SPS30_IllegalParameterError(ShdlcDeviceError):

    def __init__(self):
        super(SPS30_IllegalParameterError, 
                self).__init__(0x04, 
                        "Illegal command parameter or parameter out of allowed range")

class SPS30_ArgumentOutOfRangeError(ShdlcDeviceError):

    def __init__(self):
        super(SPS30_ArgumentOutOfRangeError, 
                self).__init__(0x28, 
                        "Internal function argument out of range")

class SPS30_NotAllowedInCurrentStateError(ShdlcDeviceError):

    def __init__(self):
        super(SPS30_NotAllowedInCurrentStateError, 
                self).__init__(0x43, 
                        "Command not allowed in current state")
