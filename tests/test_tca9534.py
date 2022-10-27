"""TCA9534 pytest module file."""

# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Gabriele Pongelli
#
# SPDX-License-Identifier: MIT

from busio import I2C

import gpio_expander


def test_tca9534_object(mock_i2c, registry_list_8_gpio):  # pylint: disable=unused-argument
    """Test registries existence."""
    _dev = gpio_expander.TCA9534(I2C(2, 3), 4)  # fake addresses
    _dev_attribs = dir(_dev)
    for _r in registry_list_8_gpio:
        assert _r in _dev_attribs


def test_tca9534_num_gpios(mock_i2c):  # pylint: disable=unused-argument
    """Check attribute return value."""
    _dev = gpio_expander.TCA9534(I2C(2, 3), 4)  # fake addresses
    assert _dev.max_gpios() == 8
