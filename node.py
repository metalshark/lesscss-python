#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Node(object):

    __slots__ = ('__code', '__parent', 'items')

    def __init__(self, code, parent):
        self.__code = code
        self.__parent = parent

        self.items = list()

    def __str__(self):
        output = ''

        selectors = self.selectors

        for key in sorted(selectors.iterkeys()):
            selector = selectors[key]

            if not selector:
                continue

            if output:
                output += '\n\n'

            output += '%s {\n' % key

            for declaration in sorted(selector.iterkeys()):
                value = selector[declaration]

                output += '  %s: %s;\n' % (declaration, value)

            output += '}'

        return output

    def __get_code(self):
        return self.__code

    def __get_parent(self):
        return self.__parent

    def __get_selectors(self):
        selectors = dict()

        try:
            names = self.names
        except AttributeError:
            pass
        else:
            for name in names:
                try:
                    selector = selectors[name]
                except KeyError:
                    selector = dict()
                    selectors[name] = selector

                declarations = self.get_declarations(name)

                for key in declarations.iterkeys():
                    value = declarations[key]
                    selector[key] = value

        for item in self.items:
            selectors.update(item.selectors)

        return selectors

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

    def get_declarations(self, selector):
        declarations = dict()

        for item in self.items:
            try:
                name, value = item.name, item.value
            except AttributeError:
                continue
            else:
                declarations[name] = value

        return declarations

    code       = property(fget=__get_code)
    parent     = property(fget=__get_parent)
    selectors  = property(fget=__get_selectors)
    statement  = property(fget=__get_statement)
    statements = property(fget=__get_statements)