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
from lesscss.lessc import compile


class TestDocsExamples(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(compile(u'div { width: 1 + 1 }'), u'div { width: 2; }')

    def test_invoke1(self):
        self.assertEqual(compile(u'a { color: blue }'), u'a { color: blue; }')

    def test_invoke2(self):
        self.assertEqual(compile(u'.post { color: blue }'),
                         u'.post { color: blue; }')

    def test_variables(self):
        self.assertEqual(compile(u'''@nice-blue: #5B83AD;
@light-blue: @nice-blue + #111;

#header { color: @light-blue; }'''), u'#header { color: #6c94be; }')

    def test_mixin(self):
        self.assertEqual(compile(u'''.bordered {
  border-top: dotted 1px black;
  border-bottom: solid 2px black;
}

#menu a {
  color: #111;
  .bordered;
}

.post a {
  color: red;
  .bordered;
}'''), '''#menu a {
  border-bottom: solid 2px black;
  border-top: dotted 1px black;
  color: #111;
}

.bordered {
  border-bottom: solid 2px black;
  border-top: dotted 1px black;
}

.post a {
  border-bottom: solid 2px black;
  border-top: dotted 1px black;
  color: red;
}''')

    def test_nested_rules(self):
        self.assertEqual(compile(u'''#header {
  color: black;

  .navigation {
    font-size: 12px;
  }
  .logo {
    width: 300px;
    :hover { text-decoration: none }
  }
}'''), u'''#header { color: black; }

#header .logo { width: 300px; }

#header .logo:hover { text-decoration: none; }

#header .navigation { font-size: 12px; }''')

    def test_operations(self):
        self.assertEqual(compile(u'''@base: 5%;
@filler: @base * 2;
@other: @base + @filler;
@base-color: #222;

* {
  padding: @base;
  width: @filler;
  margin: @other;

  color: #888 / 4;
  background-color: @base-color + #111;
  height: 100% / 2 + @filler;
}'''), u'''* {
  background-color: #333;
  color: #222;
  height: 60%;
  margin: 15%;
  padding: 5%;
  width: 10%;
}''')

    def test_units(self):
        self.assertEqual(compile(u'''@var: 1px + 5;

* {
    width: @var;
}'''), u'* { width: 6px; }')

    def test_namespaces(self):
        self.assertEqual(compile(u'''#bundle {
  .button {
    display: block;
    border: 1px solid black;
    background-color: grey;
    :hover { background-color: white }
  }
  .tab { }
  .citation { }
}

#header a {
  color: orange;
  #bundle > .button;
}'''), u'''''')

    def test_accessors(self):
        self.assertEqual(compile(u'''#defaults {
  @width: 960px;
  @color: black;
}

.article { color: #294366; }

.comment {
  width: #defaults[@width];
  color: .article['color'];
}'''), u'''.article {
  color: #294366;
}

.comment {
  color: #294366;
  width: 960px;
}''')

    def test_scope(self):
        self.assertEqual(compile(u'''@var: red;

#page {
  @var: white;
  #header {
    color: @var; // white
  }
}'''), u'''#page #header { color: white; }''')

    def test_comments(self):
        self.assertEqual(compile(u'''/* One hell of a comment */
@var: red;

// Get in line!
@var: white;'''), '')


def suite():
    test_cases = (TestDocsExamples,)
    
    suite = unittest.TestSuite()
    
    for tests in map(unittest.TestLoader().loadTestsFromTestCase, test_cases):
        suite.addTests(tests)

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
