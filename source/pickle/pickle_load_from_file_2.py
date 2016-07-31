#!/usr/bin/env python
"""Load pickles from a file
"""
#end_pymotw_header

try:
    import cPickle as pickle
except:
    import pickle
import pprint
from StringIO import StringIO
import sys

from pickle_dump_to_file_1 import SimpleObject

filename = sys.argv[1]

with open(filename, 'rb') as in_s:
    # Read the data
    while True:
        try:
            o = pickle.load(in_s)
        except EOFError:
            break
        else:
            print 'READ: %s (%s)' % (o.name, o.name_backwards)
