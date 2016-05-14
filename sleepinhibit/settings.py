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

'''The settings module.

The only public object is the get_settings() function. Everything else should be
deemed private.
'''

import json
import os
from sleepinhibit.collection import Collection

__all__ = ['get_settings']
_settings_obj = None

def get_settings():
    '''Creates, if necessary, and returns the settings object, ensuring that only one such object exists.'''
    global _settings_obj
    if _settings_obj:
        obj = _settings_obj
    else:
        obj = _SettingsObject()
        _settings_obj = obj
    return obj

class _SettingsObject(Collection):
    '''The class which stores settings. Don't create an instance directly.
    instead, use get_settings().'''
    def __init__(self):
        ''' Initialize.
        In addition to regular init, this method also initializes certain
        settings to hard-coded values, which may be overwritten by
        init_settings(), and looks for a config file at a hard-coded location.

        TODO: Factor these hard-coded items out to a file under sleepinhibit/data.
        '''
        Collection.__init__(self)
        self.config_file = '{}/.config/sleep_inhibit.json'.format(os.environ['HOME'])
        # self.managed_settings holds the settings which should be saved to disk,
        # as well as their default (initial) values.
        self.managed_settings = {'autostart': False,
                                 'battery_percent_enabled': True,
                                 'battery': True, 'batt_percent': 50,
                                 'start_inhibited': False,
                                 'icon_theme': 'dark'}
        if not os.path.isfile(self.config_file):
            with open(self.config_file, 'w') as f:
                f.write('//\n//\n{}\n')
        for key, value in self.managed_settings.items():
            Collection.__setattr__(self, key, value)
        self._init_settings()

    def _init_settings(self):
        '''Initialize settings from the config file.'''
        with open(self.config_file) as f:
            lines = f.readlines()
            data = json.loads('\n'.join(lines[2:]))
        for key, value in data.items():
            self.__setattr__(key, value)

    def save_settings(self):
        '''Save managed settings to the configuration file.

        Call this after you update a managed setting. Calling it after setting a
        non-managed setting just wastes processor cycles.'''
        output = {}
        warning = "// Sleep Inhibit Settings\n// Don't edit this file manually while the program is running lest your changes be overwritten."
        for setting in self.managed_settings.keys():
            output[setting] = self.__dict__[setting]
        with open(self.config_file, 'w') as f:
            f.write('\n'.join([warning, json.dumps(output, sort_keys=True, indent=2)]))
