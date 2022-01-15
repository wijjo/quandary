# Copyright (C) 2022, Steven Cooper
#
# This file is part of Quandary.
#
# Quandary is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Quandary is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Quandary.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys


def error(message: str):
    """
    Display error message.

    :param message: error message
    """
    sys.stderr.write(f'ERROR: {message}{os.linesep}')


def critical_error(message: str):
    """
    Display critical error message and exit.

    :param message: error message
    """
    sys.stderr.write(f'CRITICAL: {message}{os.linesep}')
    sys.exit(1)
