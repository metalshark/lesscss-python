#!/usr/bin/env python
# -*- coding: utf-8 -*-


def parse_nested(less):
    nested = ''
    
    depth = 1
    
    delimiter = ''
    
    length = len(less)

    for i in range(length):
        char = less[i]
        
        if not (char == '}' and not depth and not delimiter):
            nested += char
        
        if delimiter:
            if char == delimiter and not less[i - 1] == '\\':
                delimiter = ''
        elif char in ('"', "'"):
            delimiter = char
        elif char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            
        if not depth and not delimiter and char == '}':
            break
    else:
        raise ValueError
    
    return nested[:-1]