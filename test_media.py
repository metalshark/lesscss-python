#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from media import parse_media


class TestMedia(unittest.TestCase):
    def test_multi(self):
        self.assertEqual(parse_media('@media screen { }').media, ['screen'])
        
    def test_none(self):
        self.assertRaises(ValueError, parse_media, '@media { }')
        
    def test_single(self):
        self.assertEqual(parse_media('@media screen, print { }').media,
                         ['screen', 'print'])


def suite():
    test_cases = (TestMedia,)
    
    suite = unittest.TestSuite()
    
    for tests in map(unittest.TestLoader().loadTestsFromTestCase, test_cases):
        suite.addTests(tests)

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())