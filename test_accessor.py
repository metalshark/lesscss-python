#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from accessor import parse_accessor


class TestAccessor(unittest.TestCase):
    def test_mixin(self):
        self.assertEqual(parse_accessor('#bundle > .button;').accessor,
                         '#bundle > .button')
                         
    def test_property(self):
        self.assertEqual(parse_accessor(".article['color'];").accessor,
                         ".article['color']")
                         
    def test_variable(self):
        self.assertEqual(parse_accessor("#defaults[@width];").accessor,
                         "#defaults[@width]")


def suite():
    test_cases = (TestAccessor,)
    
    suite = unittest.TestSuite()
    
    for tests in map(unittest.TestLoader().loadTestsFromTestCase, test_cases):
        suite.addTests(tests)

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())