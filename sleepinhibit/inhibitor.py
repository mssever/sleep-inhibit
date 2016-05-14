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
This is the main module for the inhibitor process, the process which actually
prevents sleep.
'''

import subprocess
import time
from sleepinhibit import battery as battery_module
from sleepinhibit.util import cmd_output
from sleepinhibit.settings import get_settings

def run(battery=False, percent=None):
    '''The main loop for sleep inhibition.

    Args:
    battery: If True, don't inhibit sleep while running on battery
    percent: If battery == True and battery percent >= this value, go ahead and
             inhibit sleep as if running on AC.
    '''
    config = get_settings()
    minutes = config.inhibitor_interval # number of minutes of inactivity between activating keyboard
    milliseconds = minutes * 60 * 1000
    press_ctrl = ["xdotool", "key", "Control_L"]
    while True:
        curr_idle = int(cmd_output(["xprintidle"]))
        if curr_idle > milliseconds:
            if config.acpi_available and battery:
                batt = battery_module.info()
                if batt['discharging']:
                    if percent and batt['percent'] and batt['percent'] >= percent:
                        subprocess.call(press_ctrl)
                    else:
                        pass
                else:
                    subprocess.call(press_ctrl)
            else:
                subprocess.call(press_ctrl)
        time.sleep(20)
