import gpio_expander
import pytest
from busio import I2C


@pytest.fixture()
def mock_i2c(mocker):
    mocker.patch("adafruit_bus_device.i2c_device.I2CDevice", return_value=True)
    mocker.patch("busio.I2C.init")


@pytest.fixture()
def registry_list_8_gpio():
    _sub_bit = [str(x) for x in range(8)]
    _reg = ["C", "N", "I", "O"]

    _all_reg = []
    for r in _reg:
        for b in _sub_bit:
            _all_reg.append(f"{r}{b}")
    return _all_reg


@pytest.fixture()
def registry_list_16_gpio():
    _sub_bit = [str(x) for x in range(8)]
    _reg_part = ["0", "1"]
    _reg = ["C", "N", "I", "O"]

    _all_reg = []
    for r in _reg:
        for rp in _reg_part:
            for b in _sub_bit:
                _all_reg.append(f"{r}{rp}_{b}")
    return _all_reg


def test_pca9555_object(mock_i2c, registry_list_16_gpio):
    _dev = gpio_expander.PCA9555(I2C(2, 3), 4)  # fake addresses
    _dev_attribs = dir(_dev)
    for _r in registry_list_16_gpio:
        assert _r in _dev_attribs


def test_pca9555_gpio_value(mocker, mock_i2c, registry_list_16_gpio):
    mocker.patch("gpio_expander.PCA9555.GPIO0.value", return_value=True)
    _dev = gpio_expander.PCA9555(I2C(2, 3), 4)  # fake addresses

    #assert _dev.O0_0 is True
    assert _dev.GPIO0.value is True


def test_pca9535_object(mock_i2c, registry_list_16_gpio):
    _dev = gpio_expander.PCA9535(I2C(2, 3), 4)  # fake addresses
    _dev_attribs = dir(_dev)
    for _r in registry_list_16_gpio:
        assert _r in _dev_attribs


def test_tca9535_object(mock_i2c, registry_list_16_gpio):
    _dev = gpio_expander.TCA9535(I2C(2, 3), 4)  # fake addresses
    _dev_attribs = dir(_dev)
    for _r in registry_list_16_gpio:
        assert _r in _dev_attribs


def test_pca9534_object(mock_i2c, registry_list_8_gpio):
    _dev = gpio_expander.PCA9534(I2C(2, 3), 4)  # fake addresses
    _dev_attribs = dir(_dev)
    for _r in registry_list_8_gpio:
        assert _r in _dev_attribs


def test_tca9534_object(mock_i2c, registry_list_8_gpio):
    _dev = gpio_expander.TCA9534(I2C(2, 3), 4)  # fake addresses
    _dev_attribs = dir(_dev)
    for _r in registry_list_8_gpio:
        assert _r in _dev_attribs
