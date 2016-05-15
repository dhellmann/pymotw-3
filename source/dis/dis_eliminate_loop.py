#!/usr/bin/env python
# encoding: utf-8

import operator
import itertools

class Dictionary(object):

    def __init__(self, words):
        self.by_letter = {}
        self.load_data(words)

    def load_data(self, words):
        # Arrange by letter
        grouped = itertools.groupby(words, key=operator.itemgetter(0))
        # Save arranged sets of words
        self.by_letter = dict((group[0][0], group) for group in grouped)
        