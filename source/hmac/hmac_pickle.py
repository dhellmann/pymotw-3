#!/usr/bin/env python
"""Check the digests of pickles passed through a stream.
"""
#end_pymotw_header

import hashlib
import hmac
try:
    import cPickle as pickle
except:
    import pickle
import pprint
from StringIO import StringIO


def make_digest(message):
    "Return a digest for the message."
    hash = hmac.new('secret-shared-key-goes-here',
                    message,
                    hashlib.sha1)
    return hash.hexdigest()


class SimpleObject(object):
    """A very simple class to demonstrate checking digests before
    unpickling.
    """
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name


# Simulate a writable socket or pipe with StringIO
out_s = StringIO()

# Write a valid object to the stream:
#  digest\nlength\npickle
o = SimpleObject('digest matches')
pickled_data = pickle.dumps(o)
digest = make_digest(pickled_data)
header = '%s %s' % (digest, len(pickled_data))
print 'WRITING:', header
out_s.write(header + '\n')
out_s.write(pickled_data)

# Write an invalid object to the stream
o = SimpleObject('digest does not match')
pickled_data = pickle.dumps(o)
digest = make_digest('not the pickled data at all')
header = '%s %s' % (digest, len(pickled_data))
print '\nWRITING:', header
out_s.write(header + '\n')
out_s.write(pickled_data)

out_s.flush()


# Simulate a readable socket or pipe with StringIO
in_s = StringIO(out_s.getvalue())

# Read the data
while True:
    first_line = in_s.readline()
    if not first_line:
        break
    incoming_digest, incoming_length = first_line.split(' ')
    incoming_length = int(incoming_length)
    print '\nREAD:', incoming_digest, incoming_length

    incoming_pickled_data = in_s.read(incoming_length)

    actual_digest = make_digest(incoming_pickled_data)
    print 'ACTUAL:', actual_digest

    if incoming_digest != actual_digest:
        print 'WARNING: Data corruption'
    else:
        obj = pickle.loads(incoming_pickled_data)
        print 'OK:', obj
    
