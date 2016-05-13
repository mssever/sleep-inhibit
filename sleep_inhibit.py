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

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('GdkPixbuf', '2.0')
import os

from sleepinhibit.settings import get_settings
from sleepinhibit.startup import main

config = get_settings()
config.start_file = os.path.realpath(__file__)
config.program_dir = '{}/sleepinhibit'.format(os.path.dirname(os.path.realpath(__file__)))
config.desktop_filename = '{}/.config/autostart/sleep_inhibit.desktop'.format(os.environ['HOME'])
config.version = '1.0.0-beta'
config.inhibitor_interval = 3 # Value is in minutes

if __name__ == '__main__':
    exit(main())