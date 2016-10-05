#!/usr/bin/env python
"""Joining relative fragments into absolute URLs
"""
#end_pymotw_header

from urlparse import urljoin

print urljoin('http://www.example.com/path/file.html',
              'anotherfile.html')
print urljoin('http://www.example.com/path/file.html',
              '../anotherfile.html')
