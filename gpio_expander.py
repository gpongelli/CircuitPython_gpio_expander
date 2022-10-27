# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Gabriele Pongelli
#
# SPDX-License-Identifier: MIT

"""

`gpio_expander`.

================================================================================

CircuitPython helper library for gpio expanders (Texas Instrument PCA95xx and TCA95xx chips).


* Author(s): Gabriele Pongelli

Implementation Notes
--------------------

**Hardware:**

* `Texas Instrument PCA9534 <https://www.ti.com/lit/ds/symlink/pca9534.pdf>`_
* `Texas Instrument PCA9535 <https://www.ti.com/lit/ds/symlink/pca9535.pdf>`_
* `Texas Instrument PCA9555 <https://www.ti.com/lit/ds/symlink/pca9555.pdf>`_
* `Texas Instrument TCA9534 <https://www.ti.com/lit/ds/symlink/tca9534.pdf>`_
* `Texas Instrument TCA9535 <https://www.ti.com/lit/ds/symlink/tca9535.pdf>`_
* `Texas Instrument TCA9555 <https://www.ti.com/lit/ds/symlink/tca9555.pdf>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports
try:
    from busio import I2C
except ImportError:
    pass

__version__ = "0.1.0"
__repo__ = "https://github.com/gpongelli/CircuitPython_gpio_expander.git"

import adafruit_bus_device.i2c_device as i2cdevice
from adafruit_register.i2c_bit import ROBit, RWBit
from adafruit_register.i2c_bits import ROBits, RWBits
from micropython import const

# For the PCA 953X and 955X series, the chips with 8 GPIO's have these port numbers
# The chips with 16 GPIO's have the first port for each type at double these numbers
# IE The first config port is 6
_INPUT_PORT = const(0)
_OUTPUT_PORT = const(1)
_POLARITY_REGISTER = const(2)
_CONFIG_REGISTER = const(3)


def _get_registry_params(value, x):
    _name = ""
    _reg_address_multiplier = 1
    _idx = x % 8
    _adder = 0
    if value > 8:
        _reg_address_multiplier = 2
        _adder = 1
        # datasheet bit field's name has underscore in place of dot for 16 bit expander
        if x >= 8:
            _name = "1_"
        else:
            _name = "0_"

    return _name, _reg_address_multiplier, _adder, _idx


class _MetaGPIOExpander(type):
    def __new__(mcs, clsname, bases, dct, *args, **kwargs):  # pylint: disable=unused-argument,too-many-locals
        _result_dct = {}

        for key, value in dct.items():
            # variable has full qualified name
            _result_dct[key] = value

            if key == '_NUM_GPIO':
                # call to get only interesting data
                _, _width, _, _ = _get_registry_params(value, 1)
                # entire registries
                _result_dct['input_ports'] = ROBits(8 * _width, _INPUT_PORT, 0, register_width=_width)
                _result_dct['output_ports'] = RWBits(8 * _width, _OUTPUT_PORT, 0, register_width=_width)
                _result_dct['polarity_inversions'] = RWBits(8 * _width, _POLARITY_REGISTER, 0, register_width=_width)
                _result_dct['configuration_ports'] = RWBits(8 * _width, _CONFIG_REGISTER, 0, register_width=_width)

                # create single bit registries
                for x in range(value):
                    _name, _reg_address_multiplier, _adder, _idx = _get_registry_params(value, x)

                    # REGISTRY 0 and 1  INPUT PORT
                    _result_dct[f"I{_name}{_idx}"] = ROBit(_INPUT_PORT * _reg_address_multiplier + _adder, _idx)

                    # REGISTRY 2 and 3  OUTPUT PORT
                    _result_dct[f"O{_name}{_idx}"] = RWBit(_OUTPUT_PORT * _reg_address_multiplier + _adder, _idx)

                    # REGISTRY 4 and 5  POLARITY INVERSION REGISTER
                    _result_dct[f"N{_name}{_idx}"] = RWBit(_POLARITY_REGISTER * _reg_address_multiplier + _adder, _idx)

                    # REGISTRY 6 and 7  CONFIGURATION REGISTER
                    _result_dct[f"C{_name}{_idx}"] = RWBit(_CONFIG_REGISTER * _reg_address_multiplier + _adder, _idx)

        return super(_MetaGPIOExpander, mcs).__new__(mcs, clsname, bases, _result_dct)


class _BaseGPIOExpander(metaclass=_MetaGPIOExpander):
    def __init__(self, i2c_bus: I2C, address: int, **kwargs) -> None:  # pylint: disable=unused-argument
        self.i2c_device = i2cdevice.I2CDevice(i2c_bus, address)

    def max_gpios(self) -> int:
        """Return subclass' gpio number.

        :return int value from subclass's attribute.
        """
        return getattr(self, '_NUM_GPIO')


# PCA series
class PCA9534(_BaseGPIOExpander):
    """PCA9534 8-Bit I2C I/O Expander."""

    _NUM_GPIO = 8


class PCA9535(_BaseGPIOExpander):
    """PCA9535 16-Bit I2C I/O Expander."""

    _NUM_GPIO = 16


class PCA9555(_BaseGPIOExpander):
    """PCA9555 16-Bit I2C I/O Expander."""

    _NUM_GPIO = 16


# TCA series
class TCA9534(_BaseGPIOExpander):
    """TCA9534 Low-Voltage 8-Bit I2C I/O Expander."""

    _NUM_GPIO = 8


class TCA9535(_BaseGPIOExpander):
    """TCA9535 Low-Voltage 16-Bit I2C I/O Expander."""

    _NUM_GPIO = 16


class TCA9555(_BaseGPIOExpander):
    """TCA9555 Low-Voltage 16-Bit I2C I/O Expander."""

    _NUM_GPIO = 16
