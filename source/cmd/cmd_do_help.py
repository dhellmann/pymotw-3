#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id$"
#end_pymotw_header

import cmd

class HelloWorld(cmd.Cmd):
    """Simple command processor example."""
    
    def do_greet(self, person):
        if person:
            print "hi,", person
        else:
            print 'hi'
    
    def help_greet(self):
        print '\n'.join([ 'greet [person]',
                          'Greet the named person',
                          ])
    
    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    HelloWorld().cmdloop()
