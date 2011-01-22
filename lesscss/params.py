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
from property import Property


PARAM = re.compile('''
    ^
    
    \s*
    
    (?P<name>
        [^:]+?
    )
    
    (
        \s*
    
        :
    
        \s*
        
        (?P<value>
            .+?
        )

    )?
    
    \s*
    
    $
''', re.DOTALL | re.VERBOSE)


def parse_params(less):
    params = list()
    
    depth = 0
    
    delimiter = ''
    
    chunk = ''
    
    try:
        length = len(less)
    except TypeError:
        return params

    for i in range(length):
        char = less[i]
        
        if not (char == ',' and not depth and not delimiter):
            chunk += char
        
        if delimiter:
            if char == delimiter and not less[i - 1] == '\\':
                delimiter = ''
        elif char in ('"', "'"):
            delimiter = char
        elif char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
            
        if not depth and (char == ',' or i == length - 1):
            if char == ',' and i == length - 1:
                raise ValueError('Trailing param comma')
        
            match = PARAM.match(chunk)
            
            try:
                name, value = match.group('name'), match.group('value')
            except AttributeError:
                raise ValueError()
            
            if name and not value:
                value = name
                name = None
            
            param = {'code':  chunk,
                     'name':  name,
                     'value': value}
                     
            params.append(param)
            
            chunk = ''
            
    return params
    
    
class Param(Property):
    pass
