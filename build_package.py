#!/usr/bin/env python3

import argparse
import os

import sleep_inhibit  # Sets the correct version number in the global settings object

parser = argparse.ArgumentParser(description="Builds packages for sleep_inhibit")
parser.add_argument('--deb', action='store_true', help='Build a .deb source package')
args = parser.parse_args()

srcdir = os.path.dirname(os.path.realpath(__file__))

if args.deb:
    from build.deb import main
else:
    def main(*args):
        '''Error exit'''
        exit('You must specify a package type.')

main(srcdir)
