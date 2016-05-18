# Not intended to run directly
if __name__ == '__main__':
    exit('This script is intended to be imported from ../build_package.py')

import compileall
import json
import os
import time
from os.path import join
from email.utils import formatdate

from sleepinhibit.util import cmd_output
from sleepinhibit.settings import get_config

def main(basedir):
    '''Do the build. `basedir` is the project root directory.'''
    # Common variables
    config = get_config()
    if '-' in config.version:
        exit('The version number {} is incompatible with .deb packaging for an upstream. Please remove all "-" characters from the version string.'.format(config.version))
    builddir = join(basedir, 'builddir')
    srcdir = join(builddir, '{}-{}'.format('sleep-inhibit', config.version))
    staticdir = join(basedir, 'build/deb_files')
    srcfiles = [join(basedir, 'LICENSE'), join(basedir, 'README.md'),
                join(basedir, 'sleepinhibit'), join(basedir, 'sleep_inhibit.py')]
    debiandir = join(srcdir, 'debian')
    installdir = join(debiandir, 'install')
    with open(join(basedir, 'sleepinhibit', 'data', 'credits.json')) as f:
        credits = json.loads(f.read())

    # Initialize the build dir
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
            os.unlink(join(debiandir, file_))

    # Install app files into their proper locations
    for index, dir_ in enumerate(('usr/share/sleep-inhibit', 'usr/share/applications', 'usr/bin')):#'usr/lib/python3/dist-packages/sleep-inhibit'
        dir_ = join(installdir, dir_)
        os.makedirs(join(installdir, dir_))
        if index == 0:
            print(cmd_output(['cp', '-r'] + srcfiles + [dir_]))
            compileall.compile_dir(dir_, workers=3)
        elif index == 1:
            path = 'usr/share/sleep-inhibit'
            with open(join(basedir, 'sleepinhibit/data/sleep-inhibit.desktop.template')) as src:
                with open(join(installdir, dir_, 'sleep-inhibit.desktop'), 'w') as dest:
                    dest.write(src.read().format(program_path=join(path, 'sleep_inhibit.py'),
                                                 icon_path=join(path, 'sleepinhibit/img')))
            os.chmod(join(installdir, dir_, 'sleep-inhibit.desktop'), 0o755)
        elif index == 2:
            print(cmd_output(['cp', '-r', join(staticdir, 'sleep-inhibit'), join(installdir, 'usr/bin')]))
        else:
            raise RuntimeError('Iterating over the wrong number of directories')
    make_install_file(installdir, debiandir)

    # Set up files in debian/
    make_changelog(join(staticdir, 'changelog'),
                   join(debiandir, 'changelog'), credits)
    make_copyright(join(staticdir, 'copyright'),
                   join(debiandir, 'copyright'), credits)
    make_control(join(staticdir, 'control'),
                 join(debiandir, 'control'), credits)
    print(cmd_output(['cp', '-r', join(staticdir, 'rules'), debiandir]))
    os.chmod(join(debiandir, 'rules'), 0o755)

    # Run debuild
    print(cmd_output(['debuild']))
    # Errors:
    # E: sleep-inhibit: section-is-dh_make-template
    # W: sleep-inhibit: empty-binary-package

def make_changelog(src_path, dst_path, credits):
    '''Build the changelog, using the template at src_path and writing the
    result to dst_path.
    '''
    config = get_config()
    with open(src_path) as src:
        with open(dst_path, 'w') as dst:
            chlg = src.read()
            chlg = chlg.format(pkgname='sleep-inhibit', version=config.version,
                               logmsg='This is the next release.', date=formatdate(),
                               name=credits['deb_copyright'][0]['name'],
                               email=credits['deb_copyright'][0]['email'])
            dst.write(chlg)

def make_copyright(src_path, dst_path, credits):
    '''Build debian/copyright, using the template at src_path and writing the
    result to dst_path.
    '''
    with open(src_path) as src:
        with open(dst_path, 'w') as dst:
            cp = src.read()
            src_cp = ['           {} {} <{}>'.format(i['years'], i['name'],i['email']) for i in credits['copyright']]
            src_cp[0] = src_cp[0].lstrip()
            cp = cp.format(source_copyright='\n'.join(src_cp),
                           deb_copyright_year=credits['deb_copyright'][0]['years'],
                           deb_name=credits['deb_copyright'][0]['name'],
                           deb_email=credits['deb_copyright'][0]['email'])
            dst.write(cp)

def make_control(src_path, dst_path, credits):
    '''Build debian/control, using the template at src_path and writing the
    result to dst_path.
    '''
    with open(src_path) as src:
        with open(dst_path, 'w') as dst:
            dst.write(src.read().format(name=credits['deb_copyright'][0]['name'],
                                        email=credits['deb_copyright'][0]['email']))

def make_install_file(src, debdir):
    '''Build debian/install, using the source files at src and writing the
    result to debdir/sleep-inhibit.install.
    '''
    data = []
    src_discard_len = len(src)+1
    install_from_discard_len = len(os.path.split(os.path.split(src)[0])[0]) + 1
    for dirpath, dirnames, filenames in os.walk(src):
        for name in filenames:
            data.append((join(src, dirpath, name)[install_from_discard_len:],
                         os.path.dirname(join(dirpath, name)[src_discard_len:])))
    with open(join(debdir, 'sleep-inhibit.install'), 'w') as f:
        f.write('\n'.join(['{}\t{}'.format(i[0], i[1]) for i in data]))
