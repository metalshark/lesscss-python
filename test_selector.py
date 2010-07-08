#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
Copyright 2010 Beech Horn

This file is part of lesscss-python.

lesscss-python is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

lesscss-python is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with lesscss-python.  If not, see <http://www.gnu.org/licenses/>.
'''


import unittest
from selector import parse_selector


class TestMedia(unittest.TestCase):
    def test_multi(self):
        self.assertRaises(ValueError, parse_selector, '@media screen { }')
        
    def test_none(self):
        self.assertRaises(ValueError, parse_selector, '@media { }')
        
    def test_single(self):
        self.assertRaises(ValueError, parse_selector,
                          '@media screen, print { }')


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
    test_cases = (TestMedia, TestSelector)

    suite = unittest.TestSuite()

    for tests in map(unittest.TestLoader().loadTestsFromTestCase, test_cases):
        suite.addTests(tests)

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())