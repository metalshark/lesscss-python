#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from selector import parse_selector


class TestConstantDeclaration(unittest.TestCase):
    def setUp(self):
        self.selector = parse_selector('''* {
    @constant: 10px;
}''')

    def test_count(self):
        self.assertEqual(len(self.selector.constants), 1)

    def test_value(self):
        self.assertEqual(self.selector.constants['@constant'].value, '10px')


def suite():
    test_cases = (TestConstantDeclaration,)
    
    suite = unittest.TestSuite()
    
    for tests in map(unittest.TestLoader().loadTestsFromTestCase, test_cases):
        suite.addTests(tests)

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())