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
from property import parse_property


class TestAccessor(unittest.TestCase):
    def test_mixin(self):
        self.assertRaises(ValueError, parse_property, '#bundle > .button;')

    def test_property(self):
        self.assertRaises(ValueError, parse_property, ".article['color'];")

    def test_variable(self):
        self.assertRaises(ValueError, parse_property, "#defaults[@width];")


class TestAlpha(unittest.TestCase):
    def setUp(self):
        self.property = parse_property(\
"filter:progid:DXImageTransform.Microsoft.AlphaImageLoader(src='image.png');")

    def test_name(self):
        self.assertEqual(self.property.name, 'filter')

    def test_value(self):
        self.assertEqual(self.property.value, \
"progid:DXImageTransform.Microsoft.AlphaImageLoader(src='image.png')")


class TestBracesInQuotes(unittest.TestCase):
    def setUp(self):
        self.property = parse_property('quotes: "{" "}";')

    def test_name(self):
        self.assertEqual(self.property.name, 'quotes')

    def test_value(self):
        self.assertEqual(self.property.value, '"{" "}"')
        
        
class TestConstant(unittest.TestCase):
    def test_declaration(self):
        self.assertRaises(ValueError, parse_property, '@var: white;')


class TestContent(unittest.TestCase):
    def setUp(self):
        self.property = parse_property("content: '\0000A9';")

    def test_name(self):
        self.assertEqual(self.property.name, 'content')

    def test_value(self):
        self.assertEqual(self.property.value, "'\0000A9'")


class TestContentURL(unittest.TestCase):
    def setUp(self):
        self.property = parse_property('content: url(/uri);')

    def test_name(self):
        self.assertEqual(self.property.name, 'content')

    def test_value(self):
        self.assertEqual(self.property.value, 'url(/uri)')


class TestContentURLInQuotes(unittest.TestCase):
    def setUp(self):
        self.property = parse_property("content: url('/uri');")

    def test_name(self):
        self.assertEqual(self.property.name, 'content')

    def test_value(self):
        self.assertEqual(self.property.value, "url('/uri')")


class TestFont(unittest.TestCase):
    def setUp(self):
        self.property = parse_property('''src: local('Vollkorn'),
url('http://themes.googleusercontent.com/font?kit=_3YMy3W41J9lZ9YHm0HVxA')
format('truetype');''')

    def test_name(self):
        self.assertEqual(self.property.name, 'src')

    def test_value(self):
        self.assertEqual(self.property.value, '''local('Vollkorn'),
url('http://themes.googleusercontent.com/font?kit=_3YMy3W41J9lZ9YHm0HVxA')
format('truetype')''')


class TestFontFamily(unittest.TestCase):
    def setUp(self):
        self.property = parse_property("font-family: sans-serif;")

    def test_name(self):
        self.assertEqual(self.property.name, 'font-family')

    def test_value(self):
        self.assertEqual(self.property.value, 'sans-serif')


class TestLength(unittest.TestCase):
    def test_single_line(self):
        self.assertEqual(parse_property('display:block;display:none').value,
                         'block')

    def test_multi_line(self):
        self.assertEqual(parse_property('display:block;\ndisplay:none').value,
                         'block')

    def test_multi_line_value(self):
        self.assertEqual(parse_property('''src: local('Vollkorn'),
url('http://themes.googleusercontent.com/font?kit=_3YMy3W41J9lZ9YHm0HVxA')
format('truetype');
display: block;''').value,'''local('Vollkorn'),
url('http://themes.googleusercontent.com/font?kit=_3YMy3W41J9lZ9YHm0HVxA')
format('truetype')''')


def suite():
    test_cases = (TestAccessor, TestAlpha, TestBracesInQuotes, TestConstant,
                  TestContent, TestContentURL, TestContentURLInQuotes, TestFont,
                  TestFontFamily, TestLength)

    suite = unittest.TestSuite()

    for tests in map(unittest.TestLoader().loadTestsFromTestCase, test_cases):
        suite.addTests(tests)

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())