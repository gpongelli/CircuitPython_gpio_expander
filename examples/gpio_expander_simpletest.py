"""Simple tests."""

# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Gabriele Pongelli
#
# SPDX-License-Identifier: Unlicense

import board

from gpio_expander import PCA9534, PCA9555

#######################
# 16 bit I2C expander #
#######################
_pca9555 = PCA9555(board.I2C(), 0x20)

# print input 0 bit 0 value; datasheet bit field's name has underscore in place of dot for 16 bit expander
print(_pca9555.I0_0)  # pylint: disable=no-member

# configure an output port and set its value
_pca9555.C1_3 = 0
_pca9555.O1_3 = 0

# print entire configuration registry
print(_pca9555.configuration_ports)  # pylint: disable=no-member

######################
# 8 bit I2C expander #
######################
_pca9534 = PCA9534(board.I2C(), 0x30)

# print input 0 bit value
print(_pca9534.I0)  # pylint: disable=no-member

# configure an output port and set its value
_pca9555.C3 = 0  # pylint: disable=invalid-name
_pca9555.O3 = 0  # pylint: disable=invalid-name

# print entire configuration registry
print(_pca9534.configuration_ports)  # pylint: disable=no-member
