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
from nested import parse_nested
from rules import Rules


MEDIA = re.compile('''
    (?P<names>
        @media
            
        \s*
        
        (?P<media>
        
            [a-z]+
            
            \s*
            
            (
                ,
                
                \s*
                
                [a-z]+
                
                \s*
                
            )*?
        
        )
    )

    \s*

    {
''', re.DOTALL | re.IGNORECASE | re.VERBOSE)


def parse_media(less, parent=None, **kwargs):
    match = MEDIA.match(less)

    if not match:
        raise ValueError()

    media = [media.strip() for media in match.group('media').split(',')]

    matched_length = len(match.group())

    remaining_less = less[matched_length:]

    contents = parse_nested(remaining_less)

    code = match.group() + contents + '}'

    return Media(code=code, media=media, contents=contents, parent=parent)


class Media(Rules):

    __slots__ = ('__media',)

    def __init__(self, parent, code, media, contents=None):
        Rules.__init__(self, parent=parent, code=code, contents=contents)

        self.__media = media
        
    def __get_media(self):
        return self.__media

    media = property(fget=__get_media)