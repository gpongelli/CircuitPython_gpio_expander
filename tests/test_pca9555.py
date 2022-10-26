from busio import I2C

import gpio_expander


def test_pca9555_object(mock_i2c, registry_list_16_gpio):  # pylint: disable=unused-argument
    _dev = gpio_expander.PCA9555(I2C(2, 3), 4)  # fake addresses
    _dev_attribs = dir(_dev)
    for _r in registry_list_16_gpio:
        assert _r in _dev_attribs


def test_pca9555_num_gpios(mock_i2c):  # pylint: disable=unused-argument
    _dev = gpio_expander.PCA9555(I2C(2, 3), 4)  # fake addresses
    assert _dev.max_gpios() == 16
