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

    cmd_output([join(basedir, 'cleanup.py'), '--run-from-script'])
    os.mkdir(builddir)
    os.mkdir(srcdir)
    cmd_output(['cp', '-r', join(basedir, 'LICENSE'), join(basedir, 'README.md'),
                join(basedir, 'sleepinhibit'), join(basedir, 'sleep_inhibit.py'),
                srcdir])
    os.chdir(srcdir)
    print(cmd_output(['dh_make', '--indep', '--createorig', '-cgpl3',
                '--packagename=sleep-inhibit', '-y']))
