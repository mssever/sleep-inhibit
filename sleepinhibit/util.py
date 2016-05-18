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
This module contains various utility functions.
'''

import subprocess
from gi.repository import Gio, GdkPixbuf
from sleepinhibit.config import get_config

def cmd_output(*args, **kwargs):
    '''Wrap subprocess.check_output to avoid having to do conversions, strip, etc.'''
    return subprocess.check_output(*args, **kwargs).decode('utf-8').strip()

def app_icon(which, return_pixbuf=True, theme=None):
    ''' Return an icon, where which is specific to this app.
    The icon may be returned as a Pixbuf or as a string of its filename. Theme,
    if given, should be 'light' or 'dark'.'''
    if 'indicator' in which and not theme:
        raise ValueError('Indicator icons must have a theme specified')
    icon_dir = '{}/img/{{}}'.format(get_config().program_dir)
    if theme:
        icon_dir = icon_dir.format('{}/{{}}'.format(theme))
    if which == 'window_icon':
        icon = icon_dir.format('window_icon.png')
    elif which == 'indicator_sleep':
        icon = icon_dir.format('indicator_sleep.svg')
    elif which == 'indicator_no_sleep':
        icon = icon_dir.format('indicator_no_sleep.svg')
    if return_pixbuf:
        with open(icon, 'rb') as f:
            img = f.read()
        input_stream = Gio.MemoryInputStream.new_from_data(img, None)
        return GdkPixbuf.Pixbuf.new_from_stream(input_stream, None)
    else:
        return icon
