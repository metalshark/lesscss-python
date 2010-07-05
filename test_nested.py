#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from nested import parse_nested


class TestNested(unittest.TestCase):
    def test_single_depth(self):
        self.assertEqual('a', parse_nested('a}'))
        
    def test_single_depth_spaced(self):
        self.assertEqual(' a ', parse_nested(' a } '))
        
    def test_double_depth(self):
        self.assertEqual('{a}', parse_nested('{a}}'))
        
    def test_double_depth_spaced(self):
        self.assertEqual(' { a } ', parse_nested(' { a } } '))
        
    def test_triple_depth(self):
        self.assertEqual('{{a}}', parse_nested('{{a}}}'))
        
    def test_triple_depth_spaced(self):
        self.assertEqual(' { { a } } ', parse_nested(' { { a } } } '))
        
    def test_bundle(self):
        self.assertEqual(".b { :h { } } .t { ... } .c { ... } ",
                         parse_nested(".b { :h { } } .t { ... } .c { ... } }"))


def suite():
    test_cases = (TestNested,)
    
    suite = unittest.TestSuite()
    
    for tests in map(unittest.TestLoader().loadTestsFromTestCase, test_cases):
        suite.addTests(tests)

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())