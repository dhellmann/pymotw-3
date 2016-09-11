#!/usr/bin/env python3
"""Replacing os.system with subprocess.
"""
#end_pymotw_header

import subprocess

# Simple command
subprocess.call(['ls', '-1'])
