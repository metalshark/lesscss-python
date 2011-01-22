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
from lesscss.node import Node


ACCESSOR = re.compile('''
    (?P<value>
        [a-z 0-9 \- _ \* \. \s , : # &]+?
        (
            \s*
            >
            
            \s*
            [a-z 0-9 \- _ \* \. \s , : # &]+?
        )+
    |
        [a-z 0-9 \- _ \* \. \s , : # &]+?
        \[
            .+?
        \]
    )
    
    \s*
    
    (
        ;
    |
        }
    )
''', re.DOTALL | re.VERBOSE)


def parse_accessor(less, parent=None, **kwargs):
    match = ACCESSOR.match(less)
    
    if not match:
        raise ValueError()
    
    code = match.group()
    accessor = match.group('value')
    
    return Accessor(accessor=accessor, code=code, parent=parent)


class Accessor(Node):
    
    __slots__ = ('__accessor',)
    
    def __init__(self, accessor, code, parent):
        Node.__init__(self, code=code, parent=parent)
        
        self.__accessor = accessor
        
    def __get_accessor(self):
        return self.__accessor
        
    accessor = property(fget=__get_accessor)