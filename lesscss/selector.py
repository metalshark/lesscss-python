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
from lesscss.nested   import parse_nested
from lesscss.property import Property
from lesscss.rules    import Rules


SELECTOR = re.compile('''
    (?P<names>
        [a-z 0-9 \- _ \* \. \s , : # & @]+?
    )

    \s*

    {
''', re.DOTALL | re.VERBOSE)


def parse_selector(less, parent=None, **kwargs):
    match = SELECTOR.match(less)

    if not match:
        raise ValueError()
        
    names = match.group('names')
    
    if names.startswith('@media'):
        raise ValueError

    names = [name.strip() for name in names.split(',')]

    matched_length = len(match.group())

    remaining_less = less[matched_length:]

    contents = parse_nested(remaining_less)

    code = match.group() + contents + '}'

    return Selector(code=code, names=names, contents=contents, parent=parent)


class Selector(Rules):

    __slots__ = ('__names',)

    def __init__(self, parent, code, names=None, contents=None):
        Rules.__init__(self, parent=parent, code=code, contents=contents)

        self.__names = names

    def __get_names(self):
        try:
            parent_names = self.parent.names
        except AttributeError:
            return self.__names
        else:
            if not parent_names:
                return self.__names

        names = list()

        for parent_name in parent_names:
            for name in self.__names:
                if name[0] == ':':
                    name = parent_name + name
                else:
                    name = ' '.join((parent_name, name))
                name = name.replace(' &', '')

                names.append(name)

        return names

    names = property(fget=__get_names)