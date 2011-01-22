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


from constant import Constant
from node     import Node
from property import Property


class Rules(Node):

    __slots__ = ('__contents')

    def __init__(self, code, contents=None, parent=None):
        Node.__init__(self, code=code, parent=parent)

        self.__contents = contents

    def __get_contents(self):
        return self.__contents

    contents = property(fget=__get_contents)