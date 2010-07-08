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
from node import Node


IMPORT = re.compile('''
    @import
    
    \s*
    
    (
        (?P<filename>
            '.*?(?!\\\\)'
        |
            ".*?(?!\\\\)"
        )
    |
        url\(
            (?P<url>
                .*?(?!\\\\)
            )
        \)
        
        \s*
        
        (?P<media>
            [a-z \s ,]*
        )
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


def parse_import(less, parent=None, path=None, **kwargs):
    match = IMPORT.match(less)
    
    if not match:
        raise ValueError()
    
    code = match.group()
        
    filename = match.group('filename')
    
    if filename:
        # strip the quotation marks around the filename
        filename = filename[1:-1]
        
        less = read_file(filename, path)
        
        return Importer(parent, code, less)
    else:
        url = match.group('url')
        
        media = [media.strip() for media in match.group('media').split(',')]
        
        media = tuple(media)
        
        return CSSImport(parent=parent, code=code, target=media, url=url)
        
        
class CSSImport(Node):

    __slots__ = ('__target', '__url')
    
    def __init__(self, parent, code, target, url):
        Node.__init__(self, parent=parent, code=code)
        
        self.__target = target
        self.__url    = url
        
    def __get_target(self):
        return self.__target
        
    def __get_url(self):
        return self.__url
    
    target = property(fget=__get_target)
    url    = property(fget=__get_url)


class Importer(object):
    
    __slots__ = ('__less',)
    
    def __init__(self, parent, code, less):
        Node.__init__(self, parent=parent, code=code)
        
        self.__less = less

    def __get_less(self):
        return self.__less

    less = property(fget=__get_less)