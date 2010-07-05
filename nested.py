#!/usr/bin/env python
# -*- coding: utf-8 -*-


def parse_nested(less):
    depth = 1
    
    nested = ''
    
    while depth:
        pos = less.find('}') + 1
        
        if depth and not pos:
            raise ValueError()
        
        chunk = less[:pos]
        less = less[pos:]
        
        depth += chunk.count('{')
        
        depth -= 1
        
        nested += chunk
    
    return nested[:-1]