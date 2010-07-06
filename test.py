#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import test_accessor
import test_media
import test_mixin
import test_nested
import test_parse
import test_property
import test_selector


def suite():
    test_suites = (test_accessor.suite(), test_media.suite(),
                   test_mixin.suite(), test_nested.suite(), test_parse.suite(),
                   test_property.suite(), test_selector.suite())

    return unittest.TestSuite(test_suites)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())