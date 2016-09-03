#!/usr/bin/env python3
"""Copying a file
"""
#end_pymotw_header

from shutil import *
import os
import time


def show_file_info(filename):
    stat_info = os.stat(filename)
    print('\tMode    :', stat_info.st_mode)
    print('\tCreated :', time.ctime(stat_info.st_ctime))
    print('\tAccessed:', time.ctime(stat_info.st_atime))
    print('\tModified:', time.ctime(stat_info.st_mtime))


os.mkdir('example')
print('SOURCE:')
show_file_info('shutil_copy2.py')
copy2('shutil_copy2.py', 'example')
print('DEST:')
show_file_info('example/shutil_copy2.py')
