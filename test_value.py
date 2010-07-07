#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from lessc import compile


class TestAddition(unittest.TestCase):
    pass


def suite():
    test_cases = (TestAddition,)
    
    suite = unittest.TestSuite()
    
    for tests in map(unittest.TestLoader().loadTestsFromTestCase, test_cases):
        suite.addTests(tests)

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())