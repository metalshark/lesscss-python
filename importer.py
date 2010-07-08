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