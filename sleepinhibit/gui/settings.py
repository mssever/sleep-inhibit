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
from gi.repository import Gtk, Gdk, GLib
from sleepinhibit import util
from sleepinhibit.settings import get_settings

class SettingsDialog(Gtk.Window):
    
    def __init__(self, parent):
        Gtk.Window.__init__(self, title='Sleep Inhibitor Settings')
        #Gtk.Dialog.__init__(self, "Sleep Inhibitor Settings", parent, 0,
        #    (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        #self.parent = parent
        #self.set_default_size(150, 100)

        #label = Gtk.Label("This is a dialog to display additional information")

        self.parent = parent
        self.props.gravity = Gdk.Gravity.CENTER
        self.props.resizable = False
        self.set_border_width(6)
        grid = Gtk.Grid()
        grid.set_row_spacing(20)
        #grid.set_column_homogeneous(True)
        self.add(grid)
        #self.icon-name('caffeine-cup-full')
        separator = Gtk.Separator.new(Gtk.Orientation.HORIZONTAL)

        row_counter = 0

        icon = Gtk.Image.new_from_pixbuf(util.app_icon('window_icon'))
        grid.attach(icon, 0, row_counter, 2, 1)
        row_counter += 1
        
        inhibited_switch = Gtk.Switch()
        self.inhibited_switch = inhibited_switch
        inhibited_switch.set_active(parent.config.start_inhibited)
        inhibited_switch.connect('notify::active', self.on_start_inhibited_toggle)
        inhibited_label = Gtk.Label('Start Sleep Inhibitor in inhibited mode: ')
        self.inhibited_label = inhibited_label
        inhibited_label.set_halign(Gtk.Align.START)
        grid.attach(inhibited_label, 0, row_counter, 1, 1)
        grid.attach(inhibited_switch, 1, row_counter, 1, 1)
        row_counter += 1

        autostart_switch = Gtk.Switch()
        self.autostart_switch = autostart_switch
        autostart_switch.set_active(parent.config.autostart)
        autostart_switch.connect('notify::active', self.on_autostart_toggle)
        autostart_label = Gtk.Label('Automatically start Sleep Inhibitor when you log in: ')
        self.autostart_label = autostart_label
        autostart_label.set_halign(Gtk.Align.START)
        grid.attach(autostart_label, 0, row_counter, 1, 1)
        grid.attach(autostart_switch, 1, row_counter, 1, 1)
        row_counter += 1
        
        battery_switch = Gtk.Switch()
        self.battery_switch = battery_switch
        battery_switch.set_active(not parent.config.battery)
        battery_switch.connect('notify::active', self.on_battery_toggle)
        battery_label = Gtk.Label("Always inhibit sleep when on battery: ")
        self.battery_label = battery_label
        battery_label.set_halign(Gtk.Align.START)
        grid.attach(battery_label, 0, row_counter, 1, 1)
        grid.attach(battery_switch, 1, row_counter, 1, 1)
        row_counter += 1

        grid.attach(separator, 0, row_counter, 2, 1)
        row_counter += 1

        pct_enable_switch = Gtk.Switch()
        self.pct_enable_switch = pct_enable_switch
        pct_enable_switch.set_active(parent.config.battery_percent_enabled)
        pct_enable_switch.connect('notify::active', self.on_pct_enable_toggle)
        pct_enable_label = Gtk.Label("When on battery, inhibit if the battery is at least the level below: ")
        pct_enable_label.set_halign(Gtk.Align.START)
        self.pct_enable_label = pct_enable_label
        grid.attach(pct_enable_label, 0, row_counter, 1, 1)
        grid.attach(pct_enable_switch, 1, row_counter, 1, 1)
        row_counter += 1

        if parent.config.batt_percent is not None:
            pct = parent.config.batt_percent
        else:
            pct = 85
        pct_button = Gtk.SpinButton()
        self.pct_button = pct_button
        pct_adj = Gtk.Adjustment(pct, 0, 100, 5, 10, 0)
        pct_button.set_adjustment(pct_adj)
        pct_button.set_numeric = True
        pct_button.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)
        pct_button.connect('value_changed', self.on_pct_change)
        pct_button.set_value(pct)
        self.old_pct_value = pct
        pct_label = Gtk.Label('Inhibit threshhold: ')
        self.pct_label = pct_label
        pct_label.set_halign(Gtk.Align.START)
        grid.attach(pct_label, 0, row_counter, 1, 1)
        grid.attach(pct_button, 1, row_counter, 1, 1)
        row_counter += 1

        if battery_switch.props.active:
            pct_enable_switch.props.sensitive = False
            pct_enable_label.props.sensitive = False
            pct_button.props.sensitive = False 
            pct_label.props.sensitive = False
        else:
            if not pct_enable_switch.props.active:
                pct_button.props.sensitive = False
                pct_label.props.sensitive = False

    def on_start_inhibited_toggle(self, switch, gparm):
        config = get_settings()
        config.start_inhibited = switch.props.active
        config.save_settings()

    def on_autostart_toggle(self, switch, gparm):
        config = get_settings()
        filename = config.desktop_filename
        if switch.props.active:
            with open(os.path.join(config.program_dir, 'data/sleep-inhibit.desktop.template')) as f:
                file_cont = f.read()
            file_cont = file_cont.format(program_path=config.start_file,
                                         icon_path=os.path.join(config.program_dir, 'img'))
            with open(filename, 'w') as f:
                f.write(file_cont)
            os.chmod(filename, 0o755)
        else:
            os.unlink(filename)
        config.autostart = switch.props.active
        config.save_settings()

    def on_battery_toggle(self, switch, gparm):
        config = get_settings()
        config.battery = not switch.props.active
        config.save_settings()
        self.parent.restart_inhibitor()
        if not switch.props.active:
            self.pct_enable_switch.props.sensitive = True
            self.pct_enable_label.props.sensitive = True
            self.pct_button.props.sensitive = True
            self.pct_label.props.sensitive = True
        else:
            self.pct_enable_switch.props.sensitive = False
            self.pct_enable_label.props.sensitive = False
            self.pct_button.props.sensitive = False
            self.pct_label.props.sensitive = False

    def on_pct_enable_toggle(self, switch, gparm):
        config = get_settings()
        config.battery_percent_enabled = switch.props.active
        config.save_settings()
        self.parent.restart_inhibitor()
        if switch.props.active:
            self.pct_button.props.sensitive = True
            self.pct_label.props.sensitive = True
        else:
            self.pct_button.props.sensitive = False
            self.pct_label.props.sensitive = False


    def on_pct_change(self, button):
        def change_timeout():#dialog, button):
            config = get_settings()
            new_value = button.get_value_as_int()
            old_value = self.old_pct_value
            if (new_value != old_value) and (config.batt_percent != new_value):
                self.old_value = new_value
                config.batt_percent = new_value
                config.save_settings()
                self.parent.restart_inhibitor()
            return False # Prevent timeout from repeating
        GLib.timeout_add(priority=GLib.PRIORITY_DEFAULT,
                         interval=5000,
                         function=change_timeout)
