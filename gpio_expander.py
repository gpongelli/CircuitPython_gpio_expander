# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Gabriele Pongelli
#
# SPDX-License-Identifier: MIT
"""
`gpio_expander`
================================================================================

CircuitPython helper library for gpio expanders (Texas Instrument PCA95xx and TCA95xx chips).


* Author(s): Gabriele Pongelli

Implementation Notes
--------------------

**Hardware:**

* `Texas Instrument PCA9555 <https://www.ti.com/lit/ds/symlink/pca9555.pdf>_`
* `Texas Instrument PCA9535 <https://www.ti.com/lit/ds/symlink/pca9535.pdf>_`
* `Texas Instrument PCA9534 <https://www.ti.com/lit/ds/symlink/pca9534.pdf>_`
* `Texas Instrument TCA9535 <https://www.ti.com/lit/ds/symlink/tca9535.pdf>_`
* `Texas Instrument TCA9534 <https://www.ti.com/lit/ds/symlink/tca9534.pdf>_`


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies
  based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports
try:
    import typing  # pylint: disable=unused-import
    from busio import I2C
except ImportError:
    pass

__version__ = "0.0.0"
__repo__ = "https://github.com/gpongelli/CircuitPython_gpio_expander.git"

from micropython import const
import adafruit_bus_device.i2c_device as i2cdevice

from adafruit_register.i2c_bit import ROBit, RWBit
from adafruit_register.i2c_bits import ROBits, RWBits

try:
    from typing import Optional, Type, NoReturn
    from circuitpython_typing.device_drivers import I2CDeviceDriver
except ImportError:
    pass

# For the PCA 953X and 955X series, the chips with 8 GPIO's have these port numbers
# The chips with 16 GPIO's have the first port for each type at double these numbers
# IE The first config port is 6
_INPUT_PORT = const(0)
_OUTPUT_PORT = const(1)
_POLARITY_REGISTER = const(2)
_CONFIG_REGISTER = const(3)


class RWDependentBit(RWBit):
    """A default descriptor """
    dependent_bit: RWBit

    def __init__(
            self,
            register_address: int,
            bit: int,

            flag: bool,
            register_width: int = 1,
            lsb_first: bool = True
    ) -> None:
        super(RWDependentBit, self).__init__(register_address, bit, register_width, lsb_first)
        # self.__dependent_bit = dependent_bit
        self.__flag = flag

    def __set__(self, obj: I2CDeviceDriver, value: bool):
        # Pin can be set only when configuration dependent bit is equal to 0.
        if self.__flag != self.dependent_bit:  # self.__dependent_bit:
            raise AttributeError("Pin not configured as output.")
        else:
            super(RWDependentBit, self).__set__(obj, value)


class _I2cGpio:

    def __init__(self, input_reg: ROBit, output_reg: RWDependentBit, polarity_reg: RWBit, cfg_reg: RWBit):
        self.__input_reg = input_reg
        self.__output_reg = output_reg
        self.__polarity_reg = polarity_reg
        self.__cfg_reg = cfg_reg

    def _get_value(self) -> bool:
        # If a bit in configuration register is set to 1, the corresponding port pin is enabled as an input.
        # If a bit in this register is cleared to 0, the corresponding port pin is enabled as an output.
        if self.__cfg_reg:
            self.value = self.__input_reg
        else:
            self.value = self.__output_reg
        return self.value

# gpiozero InputDevice and OutputDevice compatible interfaces
    @property
    def value(self) -> bool:
        # The Input Port registers reflect the incoming logic levels of the pins, regardless of whether the pin is
        # defined as an input or an output by the Configuration register.
        return self.__input_reg

    @value.setter
    def value(self, new_val: bool) -> None:
        self.__output_reg = new_val

    def is_active(self):
        return self.value

    @property
    def active_high(self):
        pass

    @active_high.setter
    def active_high(self, value):
        pass

    def on(self):
        pass

    def off(self):
        pass

    def toggle(self):
        pass

    @property
    def configure(self) -> bool:
        return self.__cfg_reg

    @configure.setter
    def configure(self, new_value: bool) -> None:
        self.__cfg_reg = new_value


def _get_registry_params(value, x):
    _name = ""
    _reg_address_multiplier = 1
    _idx = x % 8
    _adder = 0
    if value > 8:
        _reg_address_multiplier = 2
        _adder = 1
        if x >= 8:
            _name = "1_"
        else:
            _name = "0_"

    return _name, _reg_address_multiplier, _adder, _idx


class MetaGPIOExpander(type):
    def __new__(mcs, clsname, bases, dct, *args, **kwargs):
        result_dct = {}

        for key, value in dct.items():
            # variable has full qualified name
            result_dct[key] = value

            if key == '_NUM_GPIO':
                # call to get only interesting data
                _, _width, _adder, _ = _get_registry_params(value, 1)
                # entire registries
                result_dct['input_ports'] = ROBits(8 * _width, _INPUT_PORT, 0, register_width=_width)
                result_dct['output_ports'] = RWBits(8 * _width, _OUTPUT_PORT, 0, register_width=_width)
                result_dct['polarity_inversions'] = RWBits(8 * _width, _POLARITY_REGISTER, 0, register_width=_width)
                result_dct['configuration_ports'] = RWBits(8 * _width, _CONFIG_REGISTER, 0, register_width=_width)

                # create single bit registries
                for x in range(value):
                    _name, _reg_address_multiplier, _adder, _idx = _get_registry_params(value, x)

                    _cfg_reg = RWBit(_CONFIG_REGISTER * _reg_address_multiplier + _adder, _idx)
                    _input_reg = ROBit(_INPUT_PORT * _reg_address_multiplier + _adder, _idx)
                    _output_reg = RWBit(_OUTPUT_PORT * _reg_address_multiplier + _adder, _idx)
                        # RWDependentBit(_OUTPUT_PORT * _reg_address_multiplier + _adder, _idx,
                        #                         _cfg_reg, False)
                    _polarity_reg = RWBit(_POLARITY_REGISTER * _reg_address_multiplier + _adder, _idx)

                    # GPIO object
                    # prop_name = f"GPIO{x}"
                    # result_dct[prop_name] = _I2cGpio(_input_reg, _output_reg, _polarity_reg, _cfg_reg)

                    # REGISTRY 0 and 1  INPUT PORT
                    prop_name = f"I{_name}{_idx}"
                    result_dct[prop_name] = _input_reg

                    # REGISTRY 2 and 3  OUTPUT PORT
                    prop_name = f"O{_name}{_idx}"
                    result_dct[prop_name] = _output_reg

                    # REGISTRY 4 and 5  POLARITY INVERSION REGISTER
                    prop_name = f"N{_name}{_idx}"
                    result_dct[prop_name] = _polarity_reg

                    # REGISTRY 6 and 7  CONFIGURATION REGISTER
                    prop_name = f"C{_name}{_idx}"
                    result_dct[prop_name] = _cfg_reg

        inst = super(MetaGPIOExpander, mcs).__new__(mcs, clsname, bases, result_dct)
        return inst


class BaseGPIOExpander(metaclass=MetaGPIOExpander):
    def __init__(self, i2c_bus: I2C, address: int, **kwargs) -> None:
        self.i2c_device = i2cdevice.I2CDevice(i2c_bus, address)

    def max_gpios(self):
        return getattr(self, '_GPIO_NUMBER')

# RPi.GPIO compatible interface
    def setmode(self, gpio: int) -> None:
        # Does nothing, pin already configured.
        pass

    def setup(self, gpio: int, mode: bool) -> None:
        _name, _, _, _idx = _get_registry_params(self.max_gpios(), gpio)
        setattr(self, f"C{_name}{_idx}", mode)

    def input(self, gpio: int) -> bool:
        _name, _, _, _idx = _get_registry_params(self.max_gpios(), gpio)
        return getattr(self, f"I{_name}{_idx}")

    def output(self, gpio: int, _value: bool) -> None:
        _name, _, _, _idx = _get_registry_params(self.max_gpios(), gpio)
        setattr(self, f"O{_name}{_idx}", _value)


class PCA9555(BaseGPIOExpander):
    _NUM_GPIO = 16


class PCA9535(BaseGPIOExpander):
    _NUM_GPIO = 16


class PCA9534(BaseGPIOExpander):
    _NUM_GPIO = 8


class TCA9535(BaseGPIOExpander):
    _NUM_GPIO = 16


class TCA9534(BaseGPIOExpander):
    _NUM_GPIO = 8
