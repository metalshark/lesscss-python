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
from lesscss.lessc import parse
from lesscss.rules import Rules


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


class TestConstantScope(unittest.TestCase):
    def setUp(self):
        less = '''@var: red;

#page {
  @var: white;
  #header {
    color: @var; // white
  }
}'''
        self.parsed = Rules(code=less)
        parse(less=less, parent=self.parsed)
        
    def get_page(self):
        for item in self.parsed.items:
            try:
                if item.names == ['#page']:
                    return item
            except AttributeError:
                pass
        else:
            self.fail()
        
    def get_header(self):
        for item in self.get_page().items:
            try:
                if item.names == ['#page #header']:
                    return item
            except AttributeError:
                pass
        else:
            self.fail()

    def test_root_value(self):
        self.assertEqual(self.parsed.get_value('@var'), 'red')

    def test_page_value(self):
        self.assertEqual(self.get_page().get_value('@var'), 'white')

    def test_header_value(self):
        self.assertEqual(self.get_header().get_value('@var'), 'white')
        
        
class TestCSSImport(unittest.TestCase):
    def setUp(self):
        self.css = '@import url("fancyfonts.css") screen;'
        self.parsed = Rules(code=self.css)
        parse(less=self.css, parent=self.parsed)

    def test_is_the_same(self):
        self.assertEqual(str(self.parsed), self.css)



class TestErrors(unittest.TestCase):
    def parse_less(self, less):
        parent = Rules(code=less)
        parse(less=less, parent=parent)

    def test_empty_param(self):
        self.assertRaises(ValueError, self.parse_less, '.class (,) { }')

    def test_non_mixin_id(self):
        self.assertRaises(ValueError, self.parse_less, '.class { #content; }')

    def test_non_mixin_selector(self):
        self.assertRaises(ValueError, self.parse_less, '.class { content; }')

    def test_non_mixin_wildcard(self):
        self.assertRaises(ValueError, self.parse_less, '.class { *; }')

    def test_trailing_param(self):
        self.assertRaises(ValueError, self.parse_less, '.class (@param,) { }')

    def test_unclosed_block(self):
        self.assertRaises(ValueError, self.parse_less, '.class { color: red;')

    def test_undeclared_constant(self):
        self.assertRaises(ValueError, self.parse_less, '.class { @constant; }')

    def test_unterminated_apos(self):
        self.assertRaises(ValueError, self.parse_less, ".class { content: '; }")

    def test_unterminated_string(self):
        self.assertRaises(ValueError, self.parse_less, '.class { content: "; }')


class TestFontDeclarationCorruption(unittest.TestCase):
    def setUp(self):
        self.css = '''@font-face {
  font-family: 'Cantarell';
  font-style: normal;
  font-weight: normal;
  src: local('Cantarell'), \
url('http://themes.googleusercontent.com/font?kit=tGao7ZPoloMxQHxq-2oxNA') \
format('truetype');
}'''
        self.parsed = Rules(code=self.css)
        parse(less=self.css, parent=self.parsed)

    def test_is_the_same(self):
        self.assertEqual(str(self.parsed), self.css)
        
        
class TestImport(unittest.TestCase):
    def setUp(self):
        self.css = '@import "test_file";'
        self.parsed = Rules(code=self.css)
        parse(less=self.css, parent=self.parsed)

    def test_parse(self):
        self.assertEqual(str(self.parsed), u'a { text-decoration: none; }')
        
        
class TestMediaImport(unittest.TestCase):
    def setUp(self):
        self.css = '@import "test_file" screen;'
        self.parsed = Rules(code=self.css)
        parse(less=self.css, parent=self.parsed)

    def test_parse(self):
        self.assertEqual(str(self.parsed), u'''@media screen {
a { text-decoration: none; }
}''')


class TestMedia(unittest.TestCase):
    def setUp(self):
        self.css = '''@media screen {
@font-face {
  font-family: 'Cantarell';
  font-style: normal;
  font-weight: normal;
  src: local('Cantarell'), \
url('http://themes.googleusercontent.com/font?kit=tGao7ZPoloMxQHxq-2oxNA') \
format('truetype');
}
}'''
        self.parsed = Rules(code=self.css)
        parse(less=self.css, parent=self.parsed)

    def test_is_the_same(self):
        self.assertEqual(str(self.parsed), self.css)

    def test_media_selector(self):
        self.assertEqual(self.parsed.get_selectors(media=['screen']),
                         {'@font-face': {'src': '''local('Cantarell'), \
url('http://themes.googleusercontent.com/font?kit=tGao7ZPoloMxQHxq-2oxNA') \
format('truetype')''',
                                         'font-weight': 'normal',
                                         'font-style': 'normal',
                                         'font-family': "'Cantarell'"}})

    def test_media_selectors(self):
        self.assertEqual(self.parsed.get_media_selectors(),
                         (None, ['screen']))

    def test_none_selector(self):
        self.assertEqual(self.parsed.get_selectors(), {})
        

class TestNoMedia(unittest.TestCase):
    def setUp(self):
        self.css = '@media screen { }'
        self.parsed = Rules(code=self.css)
        parse(less=self.css, parent=self.parsed)

    def test_is_the_same(self):
        self.assertEqual(str(self.parsed), '')


def suite():
    test_cases = (TestConstantDeclaration, TestConstantScope, TestCSSImport,
                  TestErrors, TestFontDeclarationCorruption, TestImport,
                  TestMedia, TestMediaImport, TestNoMedia)

    suite = unittest.TestSuite()

    for tests in map(unittest.TestLoader().loadTestsFromTestCase, test_cases):
        suite.addTests(tests)

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())