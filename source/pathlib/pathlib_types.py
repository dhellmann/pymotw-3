#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2016 Doug Hellmann.  All rights reserved.
# Written for https://pymotw.com
#
"""pathlib types
"""
#end_pymotw_header

import itertools
import os
import pathlib

root = pathlib.Path('test_files')

# Clean up from previous runs.
if root.exists():
    for f in root.iterdir():
        f.unlink()
else:
    root.mkdir()

# Create test files
(root / 'file').write_text(
    'This is a regular file', encoding='utf-8')
(root / 'symlink').symlink_to('file')
os.mkfifo(str(root / 'fifo'))

# Check the file types
to_scan = itertools.chain(
    root.iterdir(),
    [pathlib.Path('/dev/disk0'),
     pathlib.Path('/dev/console')],
)
for f in to_scan:
    print(f)
    print('Is File?             :', f.is_file())
    print('Is Dir?              :', f.is_dir())
    print('Is Link?             :', f.is_symlink())
    print('Is FIFO?             :', f.is_fifo())
    print('Is block device?     :', f.is_block_device())
    print('Is character device? :', f.is_char_device())
    print()
