#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
