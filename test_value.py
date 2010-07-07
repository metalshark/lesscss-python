#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from value import get_colour, get_value, parse_value


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
    test_cases = (TestAddition, TestColour, TestDivision, TestParse,
                  TestSubtraction)
    
    suite = unittest.TestSuite()
    
    for tests in map(unittest.TestLoader().loadTestsFromTestCase, test_cases):
        suite.addTests(tests)

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())