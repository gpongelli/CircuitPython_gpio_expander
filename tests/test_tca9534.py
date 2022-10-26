import gpio_expander
import pytest
from busio import I2C


def test_tca9534_object(mock_i2c, registry_list_8_gpio):
    _dev = gpio_expander.TCA9534(I2C(2, 3), 4)  # fake addresses
    _dev_attribs = dir(_dev)
    for _r in registry_list_8_gpio:
        assert _r in _dev_attribs
