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
from lesscss.value import get_colour, get_value, parse_value


class TestAddition(unittest.TestCase):
    def test_colour(self):
        self.assertEqual(get_value('#111 + #111', {}), '#222')


class TestColour(unittest.TestCase):
    def test_blue_lower(self):
        self.assertEqual(get_colour('#0000ff'), 'blue')
        
    def test_blue_mixed(self):
        self.assertEqual(get_colour('#0000Ff'), 'blue')
        
    def test_blue_upper(self):
        self.assertEqual(get_colour('#0000FF'), 'blue')
        
    def test_triple_lower(self):
        self.assertEqual(get_colour('#aaaaaa'), '#aaa')
        
    def test_triple_mixed(self):
        self.assertEqual(get_colour('#aAaAaA'), '#aaa')
        
    def test_triple_number(self):
        self.assertEqual(get_colour('#777777'), '#777')
        
    def test_triple_upper(self):
        self.assertEqual(get_colour('#AAAAAA'), '#aaa')
        
        
class TestDivision(unittest.TestCase):
    def test_colour(self):
        self.assertEqual(get_value('#888 / 4', {}), '#222')
        
        
class TestMultiply(unittest.TestCase):
    def test_colour(self):
        self.assertEqual(get_value('#222 * 4', {}), '#888')
    

class TestParse(unittest.TestCase):
    def setUp(self):
        self.constants = {'@nice-blue': 'blue'}

    def test_constant(self):
        self.assertEqual(parse_value('@nice-blue', self.constants),
                         [{'type': 'colour', 'value': '#0000ff'}])


class TestSubtraction(unittest.TestCase):
    def test_colour(self):
        self.assertEqual(get_value('#222 - #111', {}), '#111')


def suite():
    test_cases = (TestAddition, TestColour, TestDivision, TestMultiply,
                  TestParse, TestSubtraction)
    
    suite = unittest.TestSuite()
    
    for tests in map(unittest.TestLoader().loadTestsFromTestCase, test_cases):
        suite.addTests(tests)

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())