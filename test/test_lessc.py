#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of lesscss-python.
#
# lesscss-python is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# lesscss-python is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with lesscss-python.  If not, see <http://www.gnu.org/licenses/>.
"""

Copyright (c) 2011 Evgeny V. Generalov. 
mailto:e.generalov@gmail.com
"""

import unittest
import sys
import subprocess

from lesscss import lessc


class TestLessc(unittest.TestCase):

    def setUp(self):
        self.python = sys.executable
        self.lessc = lessc.__file__
        
    def test_should_compile_a_file(self):
        css = self._run([self.python, self.lessc, 'test_file.less'])
        self.assertEqual(css, '''a { text-decoration: none; }''')

    def test_should_compile_from_stdin(self):
        less = '''a {text-decoration: none}'''
        css = self._run([self.python, self.lessc], input=less)
        self.assertEqual(css, '''a { text-decoration: none; }''')

    def _run(self, cmd, input=None, *args, **kwargs):
        proc= subprocess.Popen(cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, *args, **kwargs)
        return ''.join(proc.communicate(input=input))


def suite():
    test_cases = (TestLessc,)
    
    suite = unittest.TestSuite()
    
    for tests in map(unittest.TestLoader().loadTestsFromTestCase, test_cases):
        suite.addTests(tests)

    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

