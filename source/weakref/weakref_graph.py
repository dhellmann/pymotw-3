#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Tools for demonstrating garbage collection
"""
#end_pymotw_header

import gc
from pprint import pprint
import weakref


class Graph(object):

    def __init__(self, name):
        self.name = name
        self.other = None

    def set_next(self, other):
        print('  {}.set_next({!r})'.format(self.name, other))
        self.other = other

    def all_nodes(self):
        "Generate the nodes in the graph sequence."
        yield self
        n = self.other
        while n and n.name != self.name:
            yield n
            n = n.other
        if n is self:
            yield n

    def __str__(self):
        return '->'.join(n.name for n in self.all_nodes())

    def __repr__(self):
        return '<{} at 0x{:x} name={}>'.format(
            self.__class__.__name__, id(self), self.name)

    def __del__(self):
        print('(Deleting {})'.format(self.name))
        self.set_next(None)


def collect_and_show_garbage():
    "Show what garbage is present."
    print('Collecting...')
    n = gc.collect()
    print('Unreachable objects:', n)
    print('Tracked Graph objects:')
    for i in gc.get_objects():
        if not isinstance(i, Graph):
            continue
        print('  {!r}'.format(i))
        for r in gc.get_referents(i):
            print('    -> {!r}'.format(r))


def demo(graph_factory):
    print('Set up graph:')
    one = graph_factory('one')
    two = graph_factory('two')
    three = graph_factory('three')
    one.set_next(two)
    two.set_next(three)
    three.set_next(one)

    print('\nGraph:')
    print('  {}'.format(one))
    collect_and_show_garbage()

    three = None
    two = None
    print('\nAfter 2 references removed:')
    print('  {}'.format(one))
    collect_and_show_garbage()

    print('\nRemoving last reference:')
    one = None
    collect_and_show_garbage()
