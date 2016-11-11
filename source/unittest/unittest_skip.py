#!/usr/bin/env python3
"""
"""

#end_pymotw_header
import sys
import unittest


class SkippingTest(unittest.TestCase):

    @unittest.skip('always skipped')
    def test(self):
        self.assertTrue(False)

    @unittest.skipIf('only runs on python 2',
                     sys.version_info[0] > 2)
    def test_python2_only(self):
        self.assertTrue(False)

    @unittest.skipUnless('only runs on macOS',
                         sys.platform == 'Darwin')
    def test_macos_only(self):
        self.assertTrue(True)

    def test_raise_skiptest(self):
        raise unittest.SkipTest('skipping via exception')
