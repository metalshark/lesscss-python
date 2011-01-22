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
from node import Node


PROPERTY = re.compile('''
    (?P<name>
        [a-z0-9\-_]+
    )
    
    \s*
    
    :
    
    \s*
    
    (?P<value>
        [^;]+?
        (
            (
                '[^']*?(?!\\\\)'
            |
                "[^"]*?(?!\\\\)"
            )
            [^;'"]+?
        )*?
    )
    
    \s*
    
    (
        ;
    |
        $
    )
''', re.DOTALL | re.VERBOSE)


def parse_property(less, parent=None, **kwargs):
    match = PROPERTY.match(less)
    
    if not match:
        raise ValueError()
        
    code = match.group()
    name = match.group('name')
    value = match.group('value')
    
    return Property(parent=parent, code=code, name=name, value=value)


class Property(Node):
    
    __slots__ = ('__name', '__value')
    
    def __init__(self, code, name, parent, value):
        Node.__init__(self, code=code, parent=parent)
        
        self.__name = name
        self.__value = value
        
    def __get_name(self):
        return self.__name
        
    def __get_value(self):
        return self.__value
        
    name  = property(fget=__get_name)
    value = property(fget=__get_value)