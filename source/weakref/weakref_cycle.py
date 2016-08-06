#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Using proxy to prevent cycles.
"""
#end_pymotw_header

import gc
from pprint import pprint
import weakref

from weakref_graph import Graph, demo, collect_and_show_garbage

gc.set_debug(gc.DEBUG_LEAK)

print('Setting up the cycle\n')
demo(Graph)

print()
gc.set_debug(gc.DEBUG_UNCOLLECTABLE)
collect_and_show_garbage()
