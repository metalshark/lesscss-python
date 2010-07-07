#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
from nested   import parse_nested
from property import Property
from rules    import Rules


SELECTOR = re.compile('''
    (?P<names>
        [a-z 0-9 \- _ \* \. \s , : # & @]+?
    )

    \s*

    {
''', re.DOTALL | re.VERBOSE)


def parse_selector(less, parent=None, **kwargs):
    match = SELECTOR.match(less)

    if not match:
        raise ValueError()
        
    names = match.group('names')
    
    if names.startswith('@media'):
        raise ValueError

    names = [name.strip() for name in names.split(',')]

    matched_length = len(match.group())

    remaining_less = less[matched_length:]

    contents = parse_nested(remaining_less)

    code = match.group() + contents + '}'

    return Selector(code=code, names=names, contents=contents, parent=parent)


class Selector(Rules):

    __slots__ = ('__names',)

    def __init__(self, parent, code, names=None, contents=None):
        Rules.__init__(self, parent=parent, code=code, contents=contents)

        self.__names = names

    def __get_names(self):
        try:
            parent_names = self.parent.names
        except AttributeError:
            return self.__names
        else:
            if not parent_names:
                return self.__names

        names = list()

        for parent_name in parent_names:
            for name in self.__names:
                if name[0] == ':':
                    name = parent_name + name
                else:
                    name = ' '.join((parent_name, name))
                name = name.replace(' &', '')

                names.append(name)

        return names

    names = property(fget=__get_names)