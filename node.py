#!/usr/bin/env python
# -*- coding: utf-8 -*-


from value import get_value


class Node(object):

    __slots__ = ('__code', '__parent', 'items')

    def __init__(self, code, parent):
        self.__code = code
        self.__parent = parent

        self.items = list()

    def __str__(self):
        output = ''

        for media in self.get_media_selectors():
            if media:
                output += '@media %s {\n' % ', '.join(media)
            
            selectors = self.get_selectors(media=media)

            for key in sorted(selectors.iterkeys()):
                selector = selectors[key]

                if not selector:
                    continue

                if output and not output[-2:] == '{\n':
                    output += '\n\n'
                    
                keys = sorted(selector.keys())
                
                if len(keys) == 1:
                    declaration = keys[0]
                    value = selector[declaration]
                
                    output += '%s { %s: %s; }' % (key, declaration, value)
                else:
                    output += '%s {\n' % key

                    for declaration in keys:
                        value = selector[declaration]

                        output += '  %s: %s;\n' % (declaration, value)

                    output += '}'
                
            if media:
                output += '\n}'

        return output

    def __get_code(self):
        return self.__code

    def __get_constants(self):
        try:
            constants = self.parent.constants
        except AttributeError:
            constants = dict()

        for item in self.items:
            try:
                name, value = item.name, item.value
            except AttributeError:
                pass
            else:
                if name[0] == '@':
                    constants[name] = value

        return constants
        
    def __get_media(self):
        try:
            return self.__media
        except AttributeError:
            pass
            
        parent = self.parent
            
        if parent:
            return parent.media
        else:
            return None

    def __get_parent(self):
        return self.__parent

    def get_declarations(self, selector):
        declarations = dict()

        for item in self.items:
            try:
                name, value = item.name, item.value
            except AttributeError:
                continue
            else:
                if name[0] != '@':
                    declarations[name] = value

        return declarations
        
    def get_media_selectors(self):
        media_selectors = list()
        
        media_selectors.append(None)
        
        try:
            media_selector = self.media
        except AttributeError:
            pass
        else:
            if media_selector not in media_selectors:
                media_selectors.append(media_selector)
        
        for item in self.items:
            for media_selector in item.get_media_selectors():
                if media_selector not in media_selectors:
                    media_selectors.append(media_selector)
        
        return tuple(media_selectors)

    def get_selectors(self, media=None):
        selectors = dict()

        if self.media == media:        
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
                        value = self.get_value(value)
                        selector[key] = value

        for item in self.items:
            selectors.update(item.get_selectors(media=media))

        return selectors

    def get_value(self, less):
        constants = self.constants

        return get_value(less, constants)

    code      = property(fget=__get_code)
    constants = property(fget=__get_constants)
    media     = property(fget=__get_media)
    parent    = property(fget=__get_parent)