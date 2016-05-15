#!/usr/bin/env python
# encoding: utf-8

import collections

class Dictionary(object):

    def __init__(self, words):
        self.by_letter = collections.defaultdict(list)
        self.load_data(words)

    def load_data(self, words):
        by_letter = self.by_letter
        for word in words:
            by_letter[word[0]].append(word)
