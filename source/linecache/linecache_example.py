#!/usr/bin/env python
#
# Copyright 2007 Doug Hellmann.
#
#
#                         All Rights Reserved
#
# Permission to use, copy, modify, and distribute this software and
# its documentation for any purpose and without fee is hereby
# granted, provided that the above copyright notice appear in all
# copies and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of Doug
# Hellmann not be used in advertising or publicity pertaining to
# distribution of the software without specific, written prior
# permission.
#
# DOUG HELLMANN DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN
# NO EVENT SHALL DOUG HELLMANN BE LIABLE FOR ANY SPECIAL, INDIRECT OR
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

"""Example use of linecache module.

See http://blog.doughellmann.com/2007/04/pymotw-linecache.html
"""

__module_id__ = '$Id$'
#end_pymotw_header

import linecache
import os
import tempfile

lorem = '''Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
Vivamus eget elit. In posuere mi non risus. Mauris id quam posuere
lectus sollicitudin varius. Praesent at mi. Nunc eu velit. Sed augue
massa, fermentum id, nonummy a, nonummy sit amet, ligula. Curabitur
eros pede, egestas at, ultricies ac, pellentesque eu, tellus. 

Sed sed odio sed mi luctus mollis. Integer et nulla ac augue convallis
accumsan. Ut felis. Donec lectus sapien, elementum nec, condimentum ac,
interdum non, tellus. Aenean viverra, mauris vehicula semper porttitor,
ipsum odio consectetuer lorem, ac imperdiet eros odio a sapien. Nulla
mauris tellus, aliquam non, egestas a, nonummy et, erat. Vivamus
sagittis porttitor eros.'''

# Create a temporary text file with some text in it
fd, temp_file_name = tempfile.mkstemp()
os.close(fd)
f = open(temp_file_name, 'wt')
try:
	f.write(lorem)
finally:
	f.close()

# Pick out the same line from source and cache.
# (Notice that linecache counts from 1)
print 'SOURCE: ', lorem.split('\n')[4]
print 'CACHE : ', linecache.getline(temp_file_name, 5).rstrip()

# Blank lines include the newline
print '\nBLANK : %r' % linecache.getline(temp_file_name, 6)

# The cache always returns a string, and uses
# an empty string to indicate a line which does
# not exist.
not_there = linecache.getline(temp_file_name, 500)
print '\nNOT THERE: %r includes %d characters' %  (not_there, len(not_there))

# Errors are even hidden if linecache cannot find the file
no_such_file = linecache.getline('this_file_does_not_exist.txt', 1)
print '\nNO FILE: ', no_such_file

# Look for the linecache module, using
# the built in sys.path search.
module_line = linecache.getline('linecache.py', 3)
print '\nMODULE : ', module_line

# Clean up
os.unlink(temp_file_name)
