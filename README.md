# Sleep Inhibitor
A small indicator to prevent your Linux computer from sleeping. It works by
creating an icon and a menu where you can choose to inhibit sleep or not. There
are preferences available to autostart, to start in inhibit mode, and to control
what Sleep Inhibit does when you're running on battery.

# Usage
No installation is needed. Simply launch `sleep_inhibit` in the base directory.
You can use the preferences dialog to configure autostart if you want.

No installation is necessary. Just:

1. Place the app directory wherever you want the app to live. Having it on your `$PATH` is *not* necessary.
2. Install the dependencies (see below)
3. From the directory you installed, run `sleep_inhibit.py`.
4. If you want the app to automatically start every time you log in, open the icon's menu, select Preferences, and enable it in the preferences window.
5. If you decide to uninstall it, quit Sleep Inhibit, then run `cleanup.py`, being sure to answer yes to all questions. Then delete the directory, and all traces will be gone.

# Dependencies
Sleep Inhibit requires `xdotool` and `xprintidle` to be installed as commands on
your `$PATH`. If you want to modify behavior based on whether you're running on
battery, you'll also need the `acpi` command available.

In Ubuntu, you can satisfy all the dependencies by issuing this command (desktop users may omit `acpi`):

    sudo apt install xdotool xprintidle acpi
