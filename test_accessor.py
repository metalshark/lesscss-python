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