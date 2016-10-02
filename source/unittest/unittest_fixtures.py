#!/usr/bin/env python3
"""A test with fixtures.
"""
#end_pymotw_header

import random
import unittest


class FixturesTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('In setUpClass()')
        cls.good_range = range(1, 10)

    @classmethod
    def tearDownClass(cls):
        print('In tearDownClass()')
        del cls.good_range

    def setUp(self):
        print('In setUp()')
        self.value = random.randint(1, 10)

    def tearDown(self):
        print('In tearDown()')
        del self.value

    def test1(self):
        print('In test1()')
        self.assertIn(self.value, self.good_range)

    def test2(self):
        print('In test2()')
        self.assertIn(self.value, self.good_range)
