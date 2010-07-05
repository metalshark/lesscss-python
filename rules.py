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
        
    def __str__(self):
        return '\n\n'.join(self.statements)
        
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
        
    def __get_declarations(self):
        constants = self.constants
    
        declarations = list()
        
        for item in self.items:
            if type(item) == Property:
                name, value = item.name, item.value
                if value.startswith('@'):
                    try:
                        value = constants[value]
                    except KeyError:
                        pass
                declaration = '  %s: %s;\n' % (name, value)
                declarations.append(declaration)
        
        return ''.join(declarations)

    constants = property(fget=__get_constants)
    contents = property(fget=__get_contents)
    declarations = property(fget=__get_declarations)