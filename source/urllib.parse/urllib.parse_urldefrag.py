#!/usr/bin/env python
"""Remove fragment portion of URL
"""
#end_pymotw_header

from urlparse import urldefrag

original = 'http://netloc/path;param?query=arg#frag'
print 'original:', original
url, fragment = urldefrag(original)
print 'url     :', url
print 'fragment:', fragment
