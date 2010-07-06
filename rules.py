#!/usr/bin/env python
# -*- coding: utf-8 -*-


from constant import Constant
from node     import Node
from property import Property


class Rules(Node):

    __slots__ = ('__contents')

    def __init__(self, code, contents=None, parent=None):
        Node.__init__(self, code=code, parent=parent)

        self.__contents = contents

    def __get_constants(self):
        try:
            constants = self.parent.constants
        except AttributeError:
            constants = dict()

        for item in self.items:
            if type(item) == Constant:
                constants[item.name] = item.value

        return constants

    def __get_contents(self):
        return self.__contents

    constants    = property(fget=__get_constants)
    contents     = property(fget=__get_contents)