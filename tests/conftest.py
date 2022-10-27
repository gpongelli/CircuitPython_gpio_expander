"""Pytest common features module."""

# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Gabriele Pongelli
#
# SPDX-License-Identifier: MIT

from typing import List

import pytest


@pytest.fixture()
def mock_i2c(mocker):
    """Common I2C mock."""
    mocker.patch("adafruit_bus_device.i2c_device.I2CDevice", return_value=True)
    mocker.patch("busio.I2C.init")


@pytest.fixture()
def registry_list_8_gpio() -> List:
    """Get registry list for 8 bit device.

    Returns:
        List of registry names.
    """
    _sub_bit = [str(x) for x in range(8)]
    _reg = ["C", "N", "I", "O"]

    _all_reg = []
    for r in _reg:
        for b in _sub_bit:
            _all_reg.append(f"{r}{b}")

    _all_reg.append('input_ports')
    _all_reg.append('output_ports')
    _all_reg.append('polarity_inversions')
    _all_reg.append('configuration_ports')

    return _all_reg


@pytest.fixture()
def registry_list_16_gpio() -> List:
    """Get registry list for 16 bit device.

    Returns:
        List of registry names.
    """
    _sub_bit = [str(x) for x in range(8)]
    _reg_part = ["0", "1"]
    _reg = ["C", "N", "I", "O"]

    _all_reg = []
    for r in _reg:
        for _part in _reg_part:
            for b in _sub_bit:
                _all_reg.append(f"{r}{_part}_{b}")

    _all_reg.append('input_ports')
    _all_reg.append('output_ports')
    _all_reg.append('polarity_inversions')
    _all_reg.append('configuration_ports')

    return _all_reg
