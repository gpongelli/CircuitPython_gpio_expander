import gpio_expander
import pytest
from busio import I2C


def test_pca9555_object(mock_i2c, registry_list_16_gpio):
    _dev = gpio_expander.PCA9555(I2C(2, 3), 4)  # fake addresses
    _dev_attribs = dir(_dev)
    for _r in registry_list_16_gpio:
        assert _r in _dev_attribs


# def test_pca9555_gpio_value(mocker, mock_i2c, registry_list_16_gpio):
#     mocker.patch("gpio_expander.PCA9555.GPIO0.value", return_value=True)
#     _dev = gpio_expander.PCA9555(I2C(2, 3), 4)  # fake addresses
#
#     #assert _dev.O0_0 is True
#     assert _dev.GPIO0.value is True


def test_pca9555_num_gpios(mock_i2c):
    _dev = gpio_expander.PCA9555(I2C(2, 3), 4)  # fake addresses
    assert 16 == _dev.max_gpios()
