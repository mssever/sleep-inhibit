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

import json
import subprocess

from gi.repository.GObject import GObject
from gi.repository import Gtk, AppIndicator3, Gdk

from sleepinhibit import util
from sleepinhibit.settings import get_settings
from sleepinhibit.gui.settings import SettingsDialog

class SleepInhibitGUI(GObject):

    def __init__(self):
        GObject.__init__(self)
        config = get_settings()
        self.inhibited = False
        self.appname = 'sleep-inhibit'
        self.icon_on = util.app_icon('indicator_no_sleep', False, config.icon_theme)
        self.icon_off = util.app_icon('indicator_sleep', False, config.icon_theme)
        self.inhibit_proc = None
        SleepInhibitGUI.instance = self
        self.settings_dialog = None
        self._add_indicator()
        win = Gtk.Window()
        win.set_default_icon(util.app_icon('window_icon'))

    def _add_indicator(self):
        self.icon_path = '{}/img'.format(get_settings().program_dir)
        self.AppInd = AppIndicator3.Indicator.new(self.appname,
                                                  self.icon_off,
                                                  AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.AppInd.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self._build_indicator_menu(self.AppInd)

    def _build_indicator_menu(self, indicator):
        menu = Gtk.Menu()

        menu_item = Gtk.MenuItem("Inhibit Sleep")
        menu.append(menu_item)
        menu_item.connect("activate", self.on_toggle)
        menu_item.show()

        menu_item = Gtk.SeparatorMenuItem()
        menu.append(menu_item)
        menu_item.show()

        menu_item = Gtk.MenuItem('Preferences')
        menu.append(menu_item)
        menu_item.connect('activate', self.on_settings)
        menu_item.show()

        menu_item = Gtk.MenuItem('About')
        menu.append(menu_item)
        menu_item.connect('activate', self.on_about)
        menu_item.show()

        menu_item = Gtk.MenuItem("Quit")
        menu.append(menu_item)
        menu_item.connect("activate", self.on_quit)
        menu_item.show()

        indicator.set_menu(menu)

    def on_toggle(self, menuitem=None):
        config = get_settings()
        self.inhibited = not self.inhibited
        if self.inhibited:
            self.set_icon_enabled(menuitem)
            open_str = [config.start_file, "--mode=inhibit-process"]
            if config.battery:
                open_str.append('--battery=True')
            if config.battery_percent_enabled and config.batt_percent:
                open_str.append('--percent={}'.format(config.batt_percent))
            self.inhibit_proc = subprocess.Popen(open_str)
        else:
            self.kill_inhibit_proc()
            self.set_icon_disabled(menuitem)
    
    def on_settings(self, *args): # *args: was menuitem
        def destroy(window, *args): # *args: was event
            self.settings_dialog = None
            window.destroy()
        if self.settings_dialog:
            self.settings_dialog.present()
        else:
            dialog = SettingsDialog(self)
            self.settings_dialog = dialog
            dialog.set_type_hint(Gdk.WindowTypeHint.DIALOG)
            dialog.connect("delete-event", destroy)
            dialog.show_all()
            dialog.present()

    def on_quit(self, *args, **kwargs): # *args: was menuitem
        if 'signal' in kwargs.keys():
            print('\nExiting...')
        if self.inhibit_proc:
            self.kill_inhibit_proc()
        exit(0)

    def on_about(self, *args): # *args: was menuitem
        config = get_settings()
        with open(config.program_dir + '/data/credits.json') as f:
            credits = json.loads(f.read())
        about = Gtk.AboutDialog()
        about.set_program_name("Sleep Inhibitor")
        about.set_version(config.version)
        about.set_comments("Prevent your computer from going to sleep.")
        #about.set_website("http://www.learngtk.org/")
        #about.set_website_label("LearnGTK Website")
        about.set_authors(credits['authors'])
        about.set_artists(credits['artists'])
        about.set_copyright(credits['copyright'])
        about.set_license_type(Gtk.License.GPL_3_0)

        about.run()
        about.destroy()


    def set_icon_disabled(self, menuitem):
        self.AppInd.set_icon(self.icon_off)
        if menuitem:
            menuitem.set_label('Inhibit Sleep')

    def set_icon_enabled(self, menuitem):
        self.AppInd.set_icon(self.icon_on)
        if menuitem:
            menuitem.set_label('Enable Sleep')

    def kill_inhibit_proc(self):
        self.inhibit_proc.terminate()
        self.inhibit_proc.wait()
        self.inhibit_proc = None

    def restart_inhibitor(self):
        if self.inhibit_proc:
            self.on_toggle()
            #time.sleep(1)
            self.on_toggle()
