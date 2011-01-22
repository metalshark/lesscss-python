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
import test_accessor
import test_compile
import test_import
import test_media
import test_mixin
import test_nested
import test_parse
import test_property
import test_selector
import test_value
import test_lessc


def suite():
    test_suites = (test_accessor.suite(), test_compile.suite(),
                   test_import.suite(), test_media.suite(), test_mixin.suite(),
                   test_nested.suite(), test_parse.suite(),
                   test_property.suite(), test_selector.suite(),
                   test_value.suite())

    return unittest.TestSuite(test_suites)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
