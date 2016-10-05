#!/usr/bin/env python
"""Parsing URLs
"""
#end_pymotw_header

from urlparse import urlsplit

url = 'http://user:pwd@NetLoc:80/p1;param/p2;param?query=arg#frag'
parsed = urlsplit(url)
print parsed
print 'scheme  :', parsed.scheme
print 'netloc  :', parsed.netloc
print 'path    :', parsed.path
print 'query   :', parsed.query
print 'fragment:', parsed.fragment
print 'username:', parsed.username
print 'password:', parsed.password
print 'hostname:', parsed.hostname, '(netloc in lowercase)'
print 'port    :', parsed.port
