#!/usr/bin/env python3
"""Copying the meta-data from one file to another
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


with open('file_to_change.txt', 'wt') as f:
    f.write('content')
os.chmod('file_to_change.txt', 0o444)

print('BEFORE:')
show_file_info('file_to_change.txt')
copystat('shutil_copystat.py', 'file_to_change.txt')
print('AFTER:')
show_file_info('file_to_change.txt')
