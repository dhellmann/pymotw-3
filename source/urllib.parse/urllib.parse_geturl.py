#!/usr/bin/env python
"""Parsing URLs
"""
#end_pymotw_header

from urlparse import urlparse

original = 'http://netloc/path;param?query=arg#frag'
print 'ORIG  :', original
parsed = urlparse(original)
print 'PARSED:', parsed.geturl()
