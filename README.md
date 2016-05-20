# Sleep Inhibitor
A small indicator to prevent your Linux computer from sleeping. It works by
creating an icon and a menu where you can choose to inhibit sleep or not. There
are preferences available to autostart, to start in inhibit mode, and to control
what Sleep Inhibit does when you're running on battery.

## Getting Sleep Inhibitor
There are several options for getting Sleep Inhibitor:

1. You can use `git` to get the most recent stable version. Run this command:

        git clone 'https://github.com/mssever/sleep-inhibit.git'

2. You can [download the most recent release](https://github.com/mssever/sleep-inhibit/releases/latest). Downloading the source `tar.gz` is best. The source `zip` may have incorrect permissions. Just extract the source and you're good to go.

## Usage
No installation is needed. Simply launch `sleep_inhibit.py` in the base directory.
You can use the preferences dialog to configure autostart if you want.

#### Detailed Instructions

1. Place the app directory wherever you want the app to live. Having it on your `$PATH` is *not* necessary.
2. Install the dependencies (see below).
3. From the directory you installed, run `sleep_inhibit.py`.
4. If you want the app to automatically start every time you log in, open the icon's menu, select Preferences, and enable it in the preferences window. (This installation won't make Sleep Inhibitor available from your system menu, so enabling autostart is recommended to prevent you from having to launch it from the command line every time. Alternatively, you can create and install a `.deb` file if your system supports it, which will add Sleep Inhibitor to the system menu. Instructions for creating a `.deb` file are below.)
5. If you decide to uninstall it, quit Sleep Inhibit, then run `cleanup.py`, being sure to answer yes to all questions. Then delete the directory, and all traces will be gone.

## Dependencies
Sleep Inhibit requires `xdotool` and `xprintidle` to be installed as commands on
your `$PATH`. If you want to modify behavior based on whether you're running on
battery, you'll also need the `acpi` command available.

In Ubuntu, you can satisfy all the dependencies by issuing this command (desktop users may omit `acpi`):

    sudo apt install xdotool xprintidle acpi

## Install from Package
Ubuntu users (and probably Debian users) can build and install a `.deb` package from the source.

1. Install build dependencies. You can remove them after the package is created, if you want.

        sudo apt install packaging-dev dpkg-deb dh-make

2. Download and extract Sleep Inhibitor, then point your terminal to the source directory.
3. Run `./build_package.py --deb` to build the package.
4. Install the resulting `.deb` file, found in the directory `builddir`. Here's one way to do it:

        gdebi-gtk builddir/*.deb
