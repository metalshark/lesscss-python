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
from nested import parse_nested


class TestNested(unittest.TestCase):
    def test_braces_in_quotes(self):
        self.assertEqual('quotes: "{" "}"', parse_nested('quotes: "{" "}"}'))
        
    def test_bundle(self):
        self.assertEqual(".b { :h { } } .t { ... } .c { ... } ",
                         parse_nested(".b { :h { } } .t { ... } .c { ... } }"))
        
    def test_open_brace_in_quotes(self):
        self.assertEqual('quotes: "}"', parse_nested('quotes: "}"}'))
        
    def test_double_depth(self):
        self.assertEqual('{a}', parse_nested('{a}}'))
        
    def test_double_depth_spaced(self):
        self.assertEqual(' { a } ', parse_nested(' { a } } '))
        
    def test_open_brace_in_quotes(self):
        self.assertEqual('quotes: "{"', parse_nested('quotes: "{"}'))

    def test_single_depth(self):
        self.assertEqual('a', parse_nested('a}'))
        
    def test_single_depth_spaced(self):
        self.assertEqual(' a ', parse_nested(' a } '))
        
    def test_triple_depth(self):
        self.assertEqual('{{a}}', parse_nested('{{a}}}'))
        
    def test_triple_depth_spaced(self):
        self.assertEqual(' { { a } } ', parse_nested(' { { a } } } '))


def suite():
    test_cases = (TestNested,)
    
    suite = unittest.TestSuite()
    
    for tests in map(unittest.TestLoader().loadTestsFromTestCase, test_cases):
        suite.addTests(tests)

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())