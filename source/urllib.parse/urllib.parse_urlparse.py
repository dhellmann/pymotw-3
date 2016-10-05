#!/usr/bin/env python
"""Parsing URLs
"""
#end_pymotw_header

from urlparse import urlparse

url = 'http://netloc/path;param?query=arg#frag'
parsed = urlparse(url)
print parsed
