#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Node(object):

    __slots__ = ('__code', '__parent', 'items')
    
    def __init__(self, code, parent):
        self.__code = code
        self.__parent = parent
        
        self.items = list()
        
    def __get_code(self):
        return self.__code
    
    def __get_parent(self):
        return self.__parent
        
    def __get_statement(self):
        pass
    
    def __get_statements(self):
        statements = list()
        
        statements.append(self.statement)
        
        for item in self.items:
            for statement in item.statements:
                statements.append(statement)
                
        for statement in statements:
            if not statement:
                statements.remove(statement)
    
        return statements
        
    code   = property(fget=__get_code)
    parent = property(fget=__get_parent)
    statement  = property(fget=__get_statement)
    statements = property(fget=__get_statements)