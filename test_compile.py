#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from lessc import compile


class TestDocsExamples(unittest.TestCase):
    def test_variables(self):
        self.assertEqual(compile(u'''@nice-blue: #5B83AD;
@light-blue: @nice-blue + #111;

#header { color: @light-blue; }'''), u'#header { color: #6c94be; }')

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

    def test_scope(self):
        self.assertEqual(compile(u'''@var: red;

#page {
  @var: white;
  #header {
    color: @var; // white
  }
}'''), u'''#page #header { color: white; }''')


def suite():
    test_cases = (TestDocsExamples,)
    
    suite = unittest.TestSuite()
    
    for tests in map(unittest.TestLoader().loadTestsFromTestCase, test_cases):
        suite.addTests(tests)

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())