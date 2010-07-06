#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from selector import parse_selector


class TestSelector(unittest.TestCase):
    def test_all(self):
        '''
        Wildcard Declarations with an asterisks should be parsed.
        '''
        self.assertEqual(parse_selector('* { }').names, ['*'])

    def test_class(self):
        '''
        Class Declarations with a dot at the beginning should be parsed.
        '''
        self.assertEqual(parse_selector('.class { }').names, ['.class'])

    def test_element(self):
        '''
        Element Declarations should be parsed.
        '''
        self.assertEqual(parse_selector('element { }').names, ['element'])

    def test_font(self):
        '''
        Font Declarations should be parsed.
        '''
        self.assertEqual(parse_selector('@font-face { }').names, ['@font-face'])

    def test_id(self):
        '''
        ID Declarations with a hash at the beginning should be parsed.
        '''
        self.assertEqual(parse_selector('#hash { }').names, ['#hash'])

    def test_media(self):
        '''
        Media Declarations should be parsed.
        '''
        self.assertEqual(parse_selector('@media { }').names, ['@media'])

    def test_mixin(self):
        '''
        Mixin Declarations should be parsed.
        '''
        self.assertRaises(ValueError, parse_selector, '.mixin () { }')

    def test_multi(self):
        '''
        Multiple Declarations should be parsed.
        '''
        self.assertEqual(parse_selector('a, b { }').names, ['a', 'b'])

    def test_nested(self):
        '''
        Nested Declarations should be parsed.
        '''
        self.assertEqual(parse_selector('a b { }').names, ['a b'])


def suite():
    test_cases = (TestSelector,)

    suite = unittest.TestSuite()

    for tests in map(unittest.TestLoader().loadTestsFromTestCase, test_cases):
        suite.addTests(tests)

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())