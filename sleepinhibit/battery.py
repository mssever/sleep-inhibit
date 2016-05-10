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

import re
from sleepinhibit.util import cmd_output

def acpi_available():
    try:
        cmd_output(['acpi'])
    except FileNotFoundError:
        return False
    return True

def info():
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
