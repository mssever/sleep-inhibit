#!/usr/bin/python3
# coding=utf-8
#
# Copyright © 2016 Scott Severance
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

'''cleanup.py

This script deletes all the cruft from the project directory and makes a clean
source directory.
'''

import os
import re
import subprocess

try:
    print(__doc__, 'Continue? [Y/n]:', sep='\n', end=' ')
    ans = input()
    cont = True
    if re.search(r'^[nN]', ans.strip()):
        cont = False
except (KeyboardInterrupt, EOFError):
    exit('Canceled')
if not cont:
    exit('Canceled')

this_dir = os.path.dirname(os.path.realpath(__file__))

patterns_to_delete = (re.compile(r'__pycache__'),
                      re.compile(r'pyc$'),
                      re.compile(r'[~]$'))

for pat in patterns_to_delete:
    for dirpath, dirnames, filenames in os.walk(this_dir, topdown=False):
        if '.git' in dirpath or 'sleepinhibit/img' in dirpath:
            continue
        for name in filenames:
            name = os.path.join(dirpath, name)
            if re.search(pat, name):
                if os.path.isfile(name):
                    os.unlink(name)
        if re.search(pat, dirpath):
            if os.path.isdir(dirpath):
                os.rmdir(dirpath)
        #print(repr((dirpath, dirnames, filenames)))

try:
    print('Deleted cruft.\n\nDelete Sleep Inhibitor configuration? [y/N]:', end=' ')
    ans = input()
    cont = False
    if re.search(r'^[yY]', ans):
        cont = True
except (KeyboardInterrupt, EOFError):
    exit('Canceled')
if not cont:
    exit(0)
cmd = ['{}/sleep_inhibit.py'.format(this_dir), '--delete']
#print(cmd)
subprocess.call(cmd)
