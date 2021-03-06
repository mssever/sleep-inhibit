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

import os
if 'DISPLAY' not in os.environ or not os.environ['DISPLAY']:
    if __name__ == '__main__':
        exit('This program must be run from a graphical (X) session, and DISPLAY must be properly set.')
    else:
        print("Many features require a graphical environment, which you don't seem to have. When importing this module, it's your responsibility to ensure that you don't call any such code.")

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('GdkPixbuf', '2.0')

from sleepinhibit.config import get_config
from sleepinhibit.startup import main

config = get_config()
config.start_file = os.path.realpath(__file__)
config.program_dir = '{}/sleepinhibit'.format(os.path.dirname(config.start_file))
config.desktop_filename = '{}/.config/autostart/sleep_inhibit.desktop'.format(os.environ['HOME'])
config.version = '1.0.2'
config.inhibitor_interval = 3 # Number of minutes of inactivity between activating keyboard

if __name__ == '__main__':
    exit(main())
