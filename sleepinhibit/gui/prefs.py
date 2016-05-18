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
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
from sleepinhibit import util
from sleepinhibit.settings import get_config

class PreferencesDialog(Gtk.Window):
    '''The code to power the preferences dialog'''

    def __init__(self, parent):
        '''Build the dialog'''
        Gtk.Window.__init__(self, title='Sleep Inhibitor Preferences')
        config = get_config()

        self.parent = parent
        self.props.gravity = Gdk.Gravity.CENTER
        self.props.resizable = False
        self.set_border_width(6)
        grid = Gtk.Grid()
        grid.set_row_spacing(20)
        self.add(grid)
        separator = Gtk.Separator.new(Gtk.Orientation.HORIZONTAL)

        row_counter = 0

        icon = Gtk.Image.new_from_pixbuf(util.app_icon('window_icon'))
        grid.attach(icon, 0, row_counter, 2, 1)
        row_counter += 1

        icon_label = Gtk.Label('Which indicator icon set do you want to use?')
        icon_label.set_halign(Gtk.Align.START)
        icon_light = Gtk.ToggleButton()
        icon_light_img = Gtk.Image.new_from_pixbuf(util.app_icon('indicator_sleep', theme='light').scale_simple(22, 22, GdkPixbuf.InterpType.BILINEAR))
        icon_light.set_image(icon_light_img)
        icon_dark = Gtk.ToggleButton()
        icon_dark.set_image(Gtk.Image.new_from_pixbuf(util.app_icon('indicator_sleep', theme='dark').scale_simple(22, 22, GdkPixbuf.InterpType.BILINEAR)))
        self.icon_light = icon_light
        self.icon_dark = icon_dark
        if config.icon_theme == 'light':
            icon_light.props.active = True
            icon_dark.props.active = False
        else:
            icon_light.props.active = False
            icon_dark.props.active = True
        icon_light.connect('notify::active', self.on_icon_light_toggled)
        icon_dark.connect('notify::active', self.on_icon_dark_toggled)
        icon_grid = Gtk.Grid()
        icon_grid.attach(icon_light, 0, 0, 1, 1)
        icon_grid.attach(icon_dark, 1, 0, 1, 1)
        grid.attach(icon_label, 0, row_counter, 1, 1)
        grid.attach(icon_grid, 1, row_counter, 1, 1)
        row_counter += 1

        inhibited_switch = Gtk.Switch()
        self.inhibited_switch = inhibited_switch
        inhibited_switch.set_active(config.start_inhibited)
        inhibited_switch.connect('notify::active', self.on_start_inhibited_toggle)
        inhibited_label = Gtk.Label('Start Sleep Inhibitor in inhibited mode: ')
        self.inhibited_label = inhibited_label
        inhibited_label.set_halign(Gtk.Align.START)
        grid.attach(inhibited_label, 0, row_counter, 1, 1)
        grid.attach(inhibited_switch, 1, row_counter, 1, 1)
        row_counter += 1

        autostart_switch = Gtk.Switch()
        self.autostart_switch = autostart_switch
        autostart_switch.set_active(config.autostart)
        autostart_switch.connect('notify::active', self.on_autostart_toggle)
        autostart_label = Gtk.Label('Automatically start Sleep Inhibitor when you log in: ')
        self.autostart_label = autostart_label
        autostart_label.set_halign(Gtk.Align.START)
        grid.attach(autostart_label, 0, row_counter, 1, 1)
        grid.attach(autostart_switch, 1, row_counter, 1, 1)
        row_counter += 1

        if not config.acpi_available:
            grid.attach(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL), 0, row_counter, 2, 1)
            acpi_label_txt = '''<big>The options below are disabled because you don't have the <tt>acpi</tt> command
installed on your system. If you want Sleep Inhibit to take the battery state into
consideration, please install the <tt>acpi</tt> command and restart Sleep Inhibit.</big>'''
            acpi_label = Gtk.Label()
            acpi_label.set_markup(acpi_label_txt)
            acpi_label.set_line_wrap(True)
            grid.attach(acpi_label, 0, row_counter+1, 2, 1)
            row_counter += 2

        battery_switch = Gtk.Switch()
        self.battery_switch = battery_switch
        battery_switch.set_active(not config.battery)
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
        pct_enable_switch.set_active(config.battery_percent_enabled)
        pct_enable_switch.connect('notify::active', self.on_pct_enable_toggle)
        pct_enable_label = Gtk.Label("When on battery, inhibit if the battery is at least the level below: ")
        pct_enable_label.set_halign(Gtk.Align.START)
        self.pct_enable_label = pct_enable_label
        grid.attach(pct_enable_label, 0, row_counter, 1, 1)
        grid.attach(pct_enable_switch, 1, row_counter, 1, 1)
        row_counter += 1

        if config.batt_percent is not None:
            pct = config.batt_percent
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

        close = Gtk.Button.new_from_stock(Gtk.STOCK_CLOSE)
        close.connect('clicked', self.on_close)
        grid.attach(close, 1, row_counter, 1, 1)
        row_counter += 1

        if battery_switch.props.active or not config.acpi_available:
            pct_enable_switch.props.sensitive = False
            pct_enable_label.props.sensitive = False
            pct_button.props.sensitive = False
            pct_label.props.sensitive = False
        else:
            if not pct_enable_switch.props.active:
                pct_button.props.sensitive = False
                pct_label.props.sensitive = False
        if not config.acpi_available:
            battery_switch.props.sensitive = False
            battery_label.props.sensitive = False

    @staticmethod
    def on_start_inhibited_toggle(switch, *args): # *args: was gparm
        '''Callback for the start inhibited switch'''
        config = get_config()
        config.start_inhibited = switch.props.active
        config.save_settings()

    @staticmethod
    def on_autostart_toggle(switch, *args): # *args: was gparm
        '''Callback for the autostart switch'''
        config = get_config()
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

    def on_battery_toggle(self, switch, *args): # *args: was gparm
        '''Callback for the inhibit sleep while on battery switch'''
        config = get_config()
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

    def on_close(self, *args): # *args: was button
        '''Callback for the close button'''
        self.hide()

    def on_icon_light_toggled(self, *args): # *args: was button, gparm
        '''Callback for the light icon toggle button'''
        with self.icon_light.freeze_notify():
            with self.icon_dark.freeze_notify():
                if self.icon_light.props.active:
                    self.icon_dark.props.active = False
                    self.set_icon_theme('light')

    def on_icon_dark_toggled(self, *args): # *args: was button, gparm
        '''Callback for the dark icon toggle button'''
        with self.icon_light.freeze_notify():
            with self.icon_dark.freeze_notify():
                if self.icon_dark.props.active:
                    self.icon_light.props.active = False
                    self.set_icon_theme('dark')

    def on_pct_enable_toggle(self, switch, *args): # *args: was gparm
        '''Callback for the battery percentage switch'''
        config = get_config()
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
        '''Callback for the battery percentage spinner'''
        def change_timeout():#dialog, button):
            config = get_config()
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

    def set_icon_theme(self, theme):
        '''Change the icon theme. Valid values are 'light' and 'dark'.'''
        config = get_config()
        if theme == 'dark':
            config.icon_theme = 'dark'
            config.save_settings()
            self.parent.icon_on = util.app_icon('indicator_no_sleep', False, 'dark')
            self.parent.icon_off = util.app_icon('indicator_sleep', False, 'dark')
        else:
            config.icon_theme = 'light'
            config.save_settings()
            self.parent.icon_on = util.app_icon('indicator_no_sleep', False, 'light')
            self.parent.icon_off = util.app_icon('indicator_sleep', False, 'light')
        if self.parent.inhibited:
            self.parent.set_icon_enabled(False)
        else:
            self.parent.set_icon_disabled(False)
