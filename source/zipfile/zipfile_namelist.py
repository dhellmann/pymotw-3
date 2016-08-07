#!/usr/bin/env python
"""Reading the names out of a ZIP archive.
"""
#end_pymotw_header

import zipfile

with zipfile.ZipFile('example.zip', 'r') as zf:
    print zf.namelist()
