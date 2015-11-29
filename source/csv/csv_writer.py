#!/usr/bin/env python
"""Example of writing a comma separated value file.
"""
#end_pymotw_header

import csv
import sys

with open(sys.argv[1], 'wt') as f:
    writer = csv.writer(f)
    writer.writerow( ('Title 1', 'Title 2', 'Title 3') )
    for i in range(3):
        writer.writerow( (i+1,
                          chr(ord('a') + i),
                          '08/%02d/07' % (i+1),
                          )
                         )

print open(sys.argv[1], 'rt').read()
