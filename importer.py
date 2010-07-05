#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, re


IMPORT = re.compile('''
    @import
    
    \s*
    
    (?P<filename>
        '[^']*?(?!\\\\)'
    |
        "[^"]*?(?!\\\\)"
    )
    
    \s*
    
    ;?
''', re.DOTALL | re.VERBOSE)


def read_file(filename, path):
    if not filename.endswith('.less'):
        filename += '.less'
        
    if path:
        filename = os.path.join(path, filename)

    handle = file(filename)
    
    return handle.read()


def parse_import(less, path, parent, **kwargs):
    match = IMPORT.match(less)
    
    if not match:
        raise ValueError()
        
    filename = match.group('filename')
    
    # strip the quotation marks around the filename
    filename = filename[1:-1]
    
    code = match.group()
    less = read_file(filename, path)
    
    return Importer(parent, code, less)


class Importer(object):
    
    __slots__ = ('__code', '__less', '__parent')
    
    def __init__(self, parent, code, less):
        self.__parent = parent
    
        self.__code = code
        self.__less = less
        
    def __get_code(self):
        return self.__code
        
    def __get_less(self):
        return self.__less
        
    code = property(fget=__get_code)
    less = property(fget=__get_less)