#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

#end_pymotw_header

import subprocess

# Command with shell expansion
subprocess.call('echo $HOME', shell=True)
