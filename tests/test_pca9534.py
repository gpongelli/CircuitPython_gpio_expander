import pytest
from busio import I2C

import gpio_expander


def test_pca9534_object(mock_i2c, registry_list_8_gpio):
    _dev = gpio_expander.PCA9534(I2C(2, 3), 4)  # fake addresses
    _dev_attribs = dir(_dev)
    for _r in registry_list_8_gpio:
        assert _r in _dev_attribs


def test_pca9534_num_gpios(mock_i2c):
    _dev = gpio_expander.PCA9534(I2C(2, 3), 4)  # fake addresses
    assert 8 == _dev.max_gpios()
