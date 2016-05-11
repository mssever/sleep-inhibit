# Sleep Inhibitor
A small indicator to prevent your Linux computer from sleeping. It works by
creating an icon and a menu where you can choose to inhibit sleep or not. There
are preferences available to autostart, to start in inhibit mode, and to control
what Sleep Inhibit does when you're running on battery.

# Usage
No installation is needed. Simply launch `sleep_inhibit` in the base directory.
You can use the preferences dialog to configure autostart if you want.

# Dependencies
Sleep Inhibit requires `xdotool` and `xprintidle` to be installed as commands on
your `$PATH`. If you want to modify behavior based on whether you're running on
battery, you'll also need the `acpi` command available.

In Ubuntu, you can satisfy all the dependencies by issuing this command (desktop users may omit `acpi`):

    sudo apt install xdotool xprintidle acpi
