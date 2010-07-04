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


if __name__ == '__main__':
    unittest.main()