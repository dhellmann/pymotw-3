#!/usr/bin/env python
# encoding: utf-8

import dis

class MyObject(object):
    """Example for dis."""
    
    CLASS_ATTRIBUTE = 'some value'
    
    def __str__(self):
        return 'MyObject(%s)' % self.name
    
    def __init__(self, name):
        self.name = name

dis.dis(MyObject)
