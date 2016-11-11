#!/usr/bin/env python3
# encoding: utf-8
"""
"""

#end_pymotw_header
import importlib

loader = importlib.find_loader('example')
print('Loader:', loader)

m = loader.load_module()
print('Module:', m)
