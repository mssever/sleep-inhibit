# Not intended to run directly
if __name__ == '__main__':
    exit('This script is intended to be imported from ../build_package.py')

import os
from os.path import join

from sleepinhibit.util import cmd_output
from sleepinhibit.settings import get_settings

def main(basedir):
    config = get_settings()
    builddir = join(basedir, 'builddir')
    srcdir = join(builddir, '{}-{}'.format('sleep-inhibit', config.version))
    staticdir = join(basedir, 'build/deb_files')
    srcfiles = [join(basedir, 'LICENSE'), join(basedir, 'README.md'),
                join(basedir, 'sleepinhibit'), join(basedir, 'sleep_inhibit.py')]
    debiandir = join(srcdir, 'debian')
    installdir = join(debiandir, 'install')

    print(cmd_output([join(basedir, 'cleanup.py'), '--run-from-script']))
    os.mkdir(builddir)
    os.mkdir(srcdir)
    print(cmd_output(['cp', '-r'] + srcfiles + [srcdir]))
    os.chdir(srcdir)
    print(cmd_output(['dh_make', '--indep', '--createorig', '-cgpl3',
                '--packagename=sleep-inhibit', '-y']))
    static_files = os.listdir(staticdir)
    for file_ in os.listdir(debiandir):
        if file_.startswith('README') or file_.endswith('.ex') or file_.endswith('.EX') or file_ in static_files:
            os.unlink(file_)
    for index, dir_ in enumerated(('usr/lib/python3/dist-packages/sleep-inhibit', 'usr/share/applications', 'usr/bin')):
        os.mkdirs(join(installdir, dir_))
        if index == 0:
            print(cmd_output(['cp', '-r'] + srcfiles + [dir_]))
        elif index == 1:
            path = 'usr/lib/python3/dist-packages/sleep-inhibit'
            with open(join(basedir, 'sleepinhibit/data/sleep-inhibit.desktop.template')) as src:
                with open(join(installdir, dir_, 'sleep-inhibit.desktop'), 'w') as dest:
                    dest.write(src.read().format(programpath=join(path, 'sleep_inhibit.py'),
                                                 iconpath=join(path, 'sleepinhibit/img/window_icon.png'))
            os.chmod(join(installdir, dir_, 'sleep-inhibit.desktop'), 0o755)
        elif index == 2:
            print(cmd_output(['cp', '-r', join(staticdir, 'sleep-inhibit'), join(installdir, 'usr/bin')]))
        else:
            raise RuntimeError('Iterating over the wrong number of directories')
    print(cmd_output(['cp', '-r'] + [join(staticdir, file_) for file_ in static_files if file_ != 'sleep-inhibit'] + [debiandir]))
    print(cmd_output(['debuild']))
