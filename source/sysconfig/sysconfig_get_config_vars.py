#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""All configuration variables.
"""
#end_pymotw_header

import sysconfig

config_values = sysconfig.get_config_vars()
print 'Found %d configuration settings' % len(config_values.keys())
print

print 'Some highlights:'

print
print '  Installation prefixes:'
print '    prefix={prefix}'.format(**config_values)
print '    exec_prefix={exec_prefix}'.format(**config_values)

print
print '  Version info:'
print '    py_version={py_version}'.format(**config_values)
print '    py_version_short={py_version_short}'.format(**config_values)
print '    py_version_nodot={py_version_nodot}'.format(**config_values)

print
print '  Base directories:'
print '    base={base}'.format(**config_values)
print '    platbase={platbase}'.format(**config_values)
print '    userbase={userbase}'.format(**config_values)
print '    srcdir={srcdir}'.format(**config_values)

print
print '  Compiler and linker flags:'
print '    LDFLAGS={LDFLAGS}'.format(**config_values)
print '    BASECFLAGS={BASECFLAGS}'.format(**config_values)
print '    Py_ENABLE_SHARED={Py_ENABLE_SHARED}'.format(**config_values)
