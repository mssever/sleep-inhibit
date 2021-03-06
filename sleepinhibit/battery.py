#!/usr/bin/python3
# coding=utf-8
#
# Copyright © 2016 Scott Severance
# Code mixed in from Caffeine Plus and Jacob Vlijm
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
Contains functions for interacting with the battery.
'''

import re
from sleepinhibit.util import cmd_output
from sleepinhibit.type_check import *

@returns(bool)
def acpi_available():
    '''Return True if the command 'acpi' is available on the system.'''
    try:
        cmd_output(['acpi'])
    except FileNotFoundError:
        return False
    return True

@returns(dict)
def info():
    '''Return a dictionary of battery info with the following keys:

    'discharging': True or False
    'percent': battery level as an int
    '''
    # Example:     Battery 0: Charging, 96%, 00:16:37 until charged
    data = cmd_output(['acpi'])
    output = {'discharging': False, 'percent': None}
    o = data.find('Discharging')
    if o >= 0:
        output['discharging'] = True
    o = re.search(r'([0-9]+)%', data)
    if o:
        output['percent'] = int(o.group(1))
    return output
