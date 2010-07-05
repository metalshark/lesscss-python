#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from lessc import parse
from rules import Rules


class TestConstantDeclaration(unittest.TestCase):
    def setUp(self):
        less = '''
@constant: 10px;

* {
    @constant: 20px;
    
    a {
        @constant: 30px;
    }
}'''
        self.parsed = Rules(code=less)
        parse(less=less, parent=self.parsed)

    def test_root_value(self):
        self.assertEqual(self.parsed.constants['@constant'], '10px')

    def test_first_value(self):
        self.assertEqual(self.parsed.items[1].constants['@constant'], '20px')

    def test_second_value(self):
        self.assertEqual(self.parsed.items[1].items[1].constants['@constant'],
                         '30px')


class TestErrors(unittest.TestCase):
    def parse_less(self, less):
        parent = Rules(code=less)
        parse(less=less, parent=parent)

    def test_unclosed_block(self):
        self.assertRaises(ValueError, self.parse_less, '.class { color: red;')


def suite():
    test_cases = (TestConstantDeclaration, TestErrors)
    
    suite = unittest.TestSuite()
    
    for tests in map(unittest.TestLoader().loadTestsFromTestCase, test_cases):
        suite.addTests(tests)

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())