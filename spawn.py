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
   
# FIXME this code stinks
def user_choice(matches):
    for idx, mat in enumerate(matches):
        print('[{}]:\t{}'.format(idx+1,mat))
    nmbr = 0
    while True:
        c = input('Your choice: ')
        try:
            nmbr = int(c)
        except:
            print('"{}" could not be parsed to a number'.format(c))
        else:
            if not nmbr-1 in range(len(matches)):
                print('{} is not one of the choices'.format(nmbr))
            else:
                return matches[nmbr-1]

def main():
    options = _parse_args()
    if options.templ_dir == '':
        options.templ_dir = '/home/{}/templates'.format(os.getlogin())
    filename = options.filename[0]
    matches = []
    for temp_file in templates_iter(options.templ_dir):
        if match_filename(filename, temp_file):
            matches.append(temp_file)

    choice = '' 
    if len(matches) == 0:
        print("No match found")
        sys.exit(-1)
    elif len(matches) == 1:
        choice = matches[0]
    else:
        choice = user_choice(matches)

    if not options.destination:
        shutil.copy(choice, '.')
    else:
        shutil.copy(choice, './' + options.destination[0])
        
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
