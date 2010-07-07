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


def suite():
    test_cases = (TestConstantDeclaration, TestErrors,
                  TestFontDeclarationCorruption, TestMedia)

    suite = unittest.TestSuite()

    for tests in map(unittest.TestLoader().loadTestsFromTestCase, test_cases):
        suite.addTests(tests)

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())