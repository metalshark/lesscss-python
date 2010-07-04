import unittest
from mixin import parse_mixin


NO_PARAMS = []


class TestDeclaredParams(unittest.TestCase):
    def setUp(self):
        self.params = parse_mixin('.mixin(@param) { }').params
        
    def test_parsed(self):
        self.assertNotEqual(self.params, NO_PARAMS)
        
    def test_name(self):
        self.assertEqual(self.params[0]['name'], '@param')
        
    def test_value(self):
        self.assertEqual(self.params[0]['value'], None)


class TestDeclaredParamsWithDefaults(unittest.TestCase):
    def setUp(self):
        self.params = parse_mixin('.mixin(@param: 1) { }').params
        
    def test_parsed(self):
        self.assertNotEqual(self.params, NO_PARAMS)
        
    def test_name(self):
        self.assertEqual(self.params[0]['name'], '@param')
        
    def test_value(self):
        self.assertEqual(self.params[0]['value'], '1')


class TestNoParams(unittest.TestCase):
    def test_declared(self):
        self.assertEqual(parse_mixin('.mixin() { }').params, NO_PARAMS)
        
    def test_used(self):
        self.assertEqual(parse_mixin('.mixin();').params, NO_PARAMS)
        
    def test_used_without_brackets(self):
        self.assertEqual(parse_mixin('.mixin;').params, NO_PARAMS)

     
class TestUsedParams(unittest.TestCase):
    def setUp(self):
        self.params = parse_mixin('.mixin(1);').params
        
    def test_used(self):
        self.assertNotEqual(self.params, NO_PARAMS)
        
    def test_used_name(self):
        self.assertEqual(self.params[0]['name'], None)
        
    def test_used_value(self):
        self.assertEqual(self.params[0]['value'], '1')


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


if __name__ == '__main__':
    unittest.main()