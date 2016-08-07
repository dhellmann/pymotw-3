#!/usr/bin/env python
"""Retrieve all of the metadata for the contents of an archive.
"""
#end_pymotw_header

import datetime
import zipfile

def print_info(archive_name):
    with zipfile.ZipFile(archive_name) as zf:
        for info in zf.infolist():
            print info.filename
            print '\tComment     :', info.comment
            mod_date = datetime.datetime(*info.date_time)
            print '\tModified    :', mod_date
            if info.create_system == 0:
                system = 'Windows'
            elif info.create_system == 3:
                system = 'Unix'
            else:
                system = 'UNKNOWN'
            print '\tSystem      :', system
            print '\tZIP version :', info.create_version
            print '\tCompressed  :', info.compress_size, 'bytes'
            print '\tUncompressed:', info.file_size, 'bytes'
            print

if __name__ == '__main__':
    print_info('example.zip')
