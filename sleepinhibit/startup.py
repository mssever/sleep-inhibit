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

from argparse import ArgumentParser
import subprocess
import os

from gi.repository import GLib

from sleepinhibit import util, battery, settings
import sleepinhibit.gui.main

def dependencies_are_satisfied():
    try:
        util.cmd_output(['xprintidle'])
        subprocess.call('xdotool', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        return False
    return True

def parse_args():
    def percentage(n):
        if n.strip()[-1] == '%':
            n = n[:-1]
        n = int(n.strip())
        if 0 <= n <= 100:
            return n
        else:
            raise TypeError('Invalid Percentage!')
    
    parser = ArgumentParser(description='''Indicator to prevent
        computer from sleeping. It depends on the commands xprintidle and
        xdotool being properly installed on your system. If they aren't
        installed already, please install them. Also, the icons are taken from
        caffeine-plus, so if it isn't installed, you will probably see a broken
        icon.''')
    inhibit = 'Start with sleep inhibited.'
    batt = '''Don't inhibit sleep when running on battery. May be combined with
        -p/--percent. IMPORTANT NOTE: This option requires the presence of the
        acpi command on your system.'''
    pct = '''When used with -b/--battery, only stop inhibiting sleep when
        running on battery and the battery charge is less than PERCENTAGE
        percent.'''
    delete = 'Delete all saved configuration and exit.'
    mode = '''NOT NORMALLY CALLED MANUALLY! The mode can be either indicator
        (default) or inhibit-process. If mode is indicator, then an indicator
        icon is created. inhibit-process is to be called by the indicator. When
        sleep is inhibited, it runs, preventing sleep.'''
    add = parser.add_argument
    add('-i', '--inhibit', metavar="True or False", type=bool, help=inhibit)
    add('-b', '--battery', metavar="True or False", type=bool, help=batt)
    add('-p', '--percent', metavar="PERCENTAGE", type=percentage, help=pct)
    add('--delete', action='store_true', help=delete)
    add('--mode', type=str, default='indicator', help=mode)
    return parser.parse_args()

def main():
    args = parse_args()
    if not dependencies_are_satisfied():
        return 'This program depends on xprintidle and xdotool being installed.'
    if args.battery and not battery.acpi_available():
        return '--battery is only available if you have the acpi command on your system.'
    if args.delete:
        config = settings.get_settings()
        for file_ in (config.config_file, config.desktop_filename):
            try:
                os.unlink(file_)
            except FileNotFoundError:
                pass
        return 0
    elif args.mode == 'indicator':
        config = settings.get_settings()
        if args.battery is not None:
            config.battery = args.battery
        if args.percent is not None:
            config.batt_percent = args.percent
        inhibitor = sleepinhibit.gui.main.SleepInhibitGUI()
        if config.start_inhibited or args.inhibit:
            inhibitor.on_toggle()
        try:
            GLib.MainLoop().run()
        except KeyboardInterrupt:
            inhibitor.on_quit(signal='SIGINT')
        return 0
    elif args.mode == 'inhibit-process':
        from sleepinhibit.inhibitor import run
        kw = {}
        print(repr(args))
        if args.battery is True:
            kw['battery'] = True
            if args.percent:
                kw['percent'] = args.percent
        try:
            run(**kw)
        except KeyboardInterrupt:
            return 0
    else:
        return 'ERROR: Invalid value for --mode!'
