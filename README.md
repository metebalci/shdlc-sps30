# SHDLC Driver for Sensirion SPS30

This Python module is developed to be used with the SPS30 Evaluation Kit (SEK-SPS30). I am using and testing it with a Raspberry Pi.

`Sps30ShdlcDevice` is implemented according to [Create a Device Class @ Sensirion SHDLC Python Driver](https://sensirion.github.io/python-shdlc-driver/custom_commands.html#creating-a-device-class).

Please check the source code for documentation.

# Install

```
pip install shdlc-sps30
```

# Usage

```
from shdlc_sps30 import Sps30ShdlcDevice

with ShdlcSerialPort(port='/dev/ttyUSB0', baudrate=115200) as port:
	device = Sps30ShdlcDevice(ShdlcConnection(port))
        serial_number = device.device_information_serial_number()
        print("serial_number: %s" % serial_number)
```

# Example

See [test.py](test.py).

```
$ ./test.py
product_type: 00080000
serial_number: 8CCABCFAE3201F49
fw: 2.2 rev: 7 shdlc: 2.0
604800
(False, False, False)
((1.2945550680160522, 4.506138324737549, 7.045137405395508, 7.552936553955078), (1.6411240100860596, 6.789977550506592, 10.12799072265625, 10.780089378356934, 10.878416061401367), 1.6299999952316284)
```
