#!/usr/bin/env python
# encoding: utf-8

import string

class Dictionary(object):

    def __init__(self, words):
        self.by_letter = dict( (letter, []) 
                                for letter in string.letters)
        self.load_data(words)

    def load_data(self, words):
        for word in words:
            self.by_letter[word[0]].append(word)
