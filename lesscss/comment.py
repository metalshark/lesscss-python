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


COMMENT = re.compile('''
    /\*
    
    (?P<comment>
        .*?
    )

    \*/
''', re.DOTALL | re.VERBOSE)


LESS_COMMENT = re.compile(r'''
    //
    
    (?P<comment>
        .*?
    )
    
    (
        \n
    |
        $
    )
''', re.VERBOSE)


def parse_comment(less, parent, **kwargs):
    match = COMMENT.match(less)
    
    if not match:
        match = LESS_COMMENT.match(less)
    
    if not match:
        raise ValueError()
    
    code = match.group()
    comment = match.group('comment')
    
    return Comment(code=code, comment=comment, parent=parent)


class Comment(Node):
    
    __slots__ = ('__comment',)
    
    def __init__(self, code, comment, parent):
        Node.__init__(self, code=code, parent=parent)
        
        self.__comment = comment
        
    def __get_comment(self):
        return self.__comment
        
    comment = property(fget=__get_comment)
