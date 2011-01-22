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


import re
from nested   import parse_nested
from params   import Param, parse_params
from property import Property
from rules    import Rules


MIXIN = re.compile('''
    (?P<name>
        \.
        [a-z 0-9 \- _ \* \s , :]+
    )

    \s*

    (
        (?P<param_detect>
            \(

            (?P<params>
                .*?
            )
        )

        \)

        \s*
    )?

    \s*

    (
        (?P<nested>
            {
        )
    |
        ;
    |
        }
    )
''', re.DOTALL | re.VERBOSE)


def parse_mixin(less, parent=None, **kwargs):
    match = MIXIN.match(less)

    if not match:
        raise ValueError()

    code = match.group()

    contents = None

    if match.group('nested'):
        matched_length = len(match.group())

        remaining_less = less[matched_length:]

        contents = parse_nested(remaining_less)

        code += contents + '}'

    params = parse_params(match.group('params'))

    if contents:
        for param in params:
            if param['value'] and not param['name']:
                param['name'] = param['value']
                param['value'] = None

    name = match.group('name')

    if match.group('nested') and not match.group('param_detect'):
        raise ValueError()

    return Mixin(parent=parent, code=code, name=name, params=params,
                 contents=contents)


class Mixin(Rules):

    __slots__ = ['__name', '__params']

    def __init__(self, parent, code, name, params, contents):
        Rules.__init__(self, parent=parent, code=code, contents=contents)

        self.__name = name
        self.__params = list()

        for param in params:
            param = Param(code=param['code'],
                          name=param['name'],
                          value=param['value'],
                          parent=self)

            self.__params.append(param)

    def __get_name(self):
        return self.__name

    def __get_params(self):
        return self.__params

    name = property(fget=__get_name)
    params = property(fget=__get_params)
