#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import glob
import re
import sys
import shutil

def templates_iter(templ_dir):
    if templ_dir[-1] != '/':
        templ_dir += '/'
    return glob.iglob(templ_dir + '*')

def match_filename(pattern, filepath):
    return re.search(pattern + '[^/]+$', filepath)
    

def main():
    options = _parse_args()
    if options.templ_dir == '':
        options.templ_dir = '/home/{}/templates'.format(os.getlogin())
    filename = options.filename[0]
    matches = []
    for temp_file in templates_iter(options.templ_dir):
        if match_filename(filename, temp_file):
            matches.append(temp_file)
        if len(matches) > 1:
            print("Filename ambiguous: {}".format(matches))
            sys.exit(-2)
    if len(matches) == 0:
        print("No match found")
        sys.exit(-1)
    else:
        if options.destination[0] == '':
            shutil.copy(matches[0], '.')
        else:
            shutil.copy(matches[0], './' + options.destination[0])
        
def _parse_args():
    '''
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    '''
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('filename', type=str, help='part of a filename'
        'to be used as template', nargs=1)
    parser.add_argument('destination', type=str, help='destination'
        'filename', default='', nargs='*')
    parser.add_argument('-d', '--template-directory', dest='templ_dir', type=str,
            metavar='DIR', action='store', default='')
    options = parser.parse_args()

    return options

if __name__ == '__main__':
    main()
