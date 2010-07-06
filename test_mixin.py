#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from mixin import parse_mixin


NO_PARAMS = []


class TestBracedParams(unittest.TestCase):
    def setUp(self):
        self.params = parse_mixin(".mixin('{');").params

    def test_parsed(self):
        self.assertNotEqual(self.params, NO_PARAMS)

    def test_name(self):
        self.assertEqual(self.params[0].name, None)

    def test_value(self):
        self.assertEqual(self.params[0].value, "'{'")


class TestDeclaredBracedParams(unittest.TestCase):
    def setUp(self):
        self.params = parse_mixin(".mixin(@param: '{') { };").params

    def test_parsed(self):
        self.assertNotEqual(self.params, NO_PARAMS)

    def test_name(self):
        self.assertEqual(self.params[0].name, '@param')

    def test_value(self):
        self.assertEqual(self.params[0].value, "'{'")


class TestDeclaredParams(unittest.TestCase):
    def setUp(self):
        self.params = parse_mixin('.mixin(@param) { }').params

    def test_parsed(self):
        self.assertNotEqual(self.params, NO_PARAMS)

    def test_name(self):
        self.assertEqual(self.params[0].name, '@param')

    def test_value(self):
        self.assertEqual(self.params[0].value, None)


class TestDeclaredParamsWithDefaults(unittest.TestCase):
    def setUp(self):
        self.params = parse_mixin('.mixin(@param: 1) { }').params

    def test_parsed(self):
        self.assertNotEqual(self.params, NO_PARAMS)

    def test_name(self):
        self.assertEqual(self.params[0].name, '@param')

    def test_value(self):
        self.assertEqual(self.params[0].value, '1')


class TestDynamic(unittest.TestCase):
    def setUp(self):
        self.mixin = parse_mixin('''.fs (@main: 'TitilliumText15L400wt') {
    font-family: @main, 'Helvetica', sans-serif;
}''')

    def test_contents(self):
        self.assertEqual(self.mixin.contents, '''
    font-family: @main, 'Helvetica', sans-serif;
''')

    def test_param_name(self):
        self.assertEqual(self.mixin.params[0].name, '@main')

    def test_param_value(self):
        self.assertEqual(self.mixin.params[0].value, "'TitilliumText15L400wt'")


class TestEscaped(unittest.TestCase):
    def setUp(self):
        self.params = parse_mixin('''.mixin (@name: 'a\'', @b: 'b') {
    display: none;
}''').params

    def test_first_param_name(self):
        self.assertEqual(self.params[0].name, "@name")

    def test_first_param_value(self):
        self.assertEqual(self.params[0].value, "'a\''")

    def test_second_param_name(self):
        self.assertEqual(self.params[1].name, "@b")

    def test_first_param_value(self):
        self.assertEqual(self.params[1].value, "'b'")


class TestNestedParams(unittest.TestCase):
    def setUp(self):
        self.mixin = parse_mixin('''.box-shadow(0 2px 5px rgba(0, 0, 0, 0.125),
0 2px 10px rgba(0, 0, 0, 0.25));''')

    def test_count(self):
        self.assertEqual(len(self.mixin.params), 2)

    def test_first_param_name(self):
        self.assertEqual(self.mixin.params[0].name, None)

    def test_first_param_value(self):
        self.assertEqual(self.mixin.params[0].value,
                         '0 2px 5px rgba(0, 0, 0, 0.125)')

    def test_second_param_name(self):
        self.assertEqual(self.mixin.params[1].name, None)

    def test_second_param_value(self):
        self.assertEqual(self.mixin.params[1].value,
                         '0 2px 10px rgba(0, 0, 0, 0.25)')


class TestNoParams(unittest.TestCase):
    def test_declared(self):
        self.assertEqual(parse_mixin('.mixin() { }').params, NO_PARAMS)

    def test_used(self):
        self.assertEqual(parse_mixin('.mixin();').params, NO_PARAMS)

    def test_used_without_brackets(self):
        self.assertEqual(parse_mixin('.mixin;').params, NO_PARAMS)


class TestNotMixin(unittest.TestCase):
    def test_all(self):
        '''
        Wildcard Declarations with an asterisks should not be parsed.
        '''
        self.assertRaises(ValueError, parse_mixin, '* { }')

    def test_class(self):
        '''
        Class Declarations with a dot at the beginning should not be parsed.
        '''
        self.assertRaises(ValueError, parse_mixin, '.class { }')

    def test_element(self):
        '''
        Element Declarations should not be parsed.
        '''
        self.assertRaises(ValueError, parse_mixin, 'element { }')

    def test_id(self):
        '''
        ID Declarations with a hash at the beginning should not be parsed.
        '''
        self.assertRaises(ValueError, parse_mixin, '#hash { }')


class TestUsedParams(unittest.TestCase):
    def setUp(self):
        self.params = parse_mixin('.mixin(1);').params

    def test_used(self):
        self.assertNotEqual(self.params, NO_PARAMS)

    def test_used_name(self):
        self.assertEqual(self.params[0].name, None)

    def test_used_value(self):
        self.assertEqual(self.params[0].value, '1')


def suite():
    test_cases = (TestBracedParams, TestDeclaredBracedParams,
                  TestDeclaredParams, TestDeclaredParamsWithDefaults,
                  TestDynamic, TestEscaped, TestNestedParams, TestNoParams,
                  TestNotMixin, TestUsedParams)

    suite = unittest.TestSuite()

    for tests in map(unittest.TestLoader().loadTestsFromTestCase, test_cases):
        suite.addTests(tests)

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())