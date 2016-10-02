#!/usr/bin/env python3
"""Simplistic examples of unit tests.
"""
#end_pymotw_header

import unittest


class SimplisticTest(unittest.TestCase):

    def test(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
