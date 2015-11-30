#!/usr/bin/env python
"""Example of writing a comma separated value file.
"""
#end_pymotw_header

import csv
import sys

fieldnames = ('Title 1', 'Title 2', 'Title 3')
headers = {
    n: n
    for n in fieldnames
}

with open(sys.argv[1], 'wt') as f:

    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(3):
        writer.writerow({
            'Title 1': i + 1,
            'Title 2': chr(ord('a') + i),
            'Title 3': '08/%02d/07' % (i + 1),
        })

print(open(sys.argv[1], 'rt').read())
