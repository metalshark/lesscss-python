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


from value import get_value


class Node(object):

    __slots__ = ('__code', '__parent', 'items')

    def __init__(self, code, parent):
        self.__code = code
        self.__parent = parent

        self.items = list()

    def __str__(self):
        output = ''
        
        imports = self.get_imports()
        
        for url in imports.iterkeys():
            if output:
                output += '\n\n'
                
            output += '@import url(%s) %s;' % (url, ', '.join(imports[url]))

        for media in self.get_media_selectors():
            selectors = self.get_selectors(media=media)
        
            if not selectors:
                continue
        
            if media:
                output += '@media %s {\n' % ', '.join(media)

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

    def get_declarations(self):
        declarations = dict()

        for item in self.items:
            try:
                name, value = item.name, item.value
            except AttributeError:
                pass
            else:
                if name[0] != '@':
                    declarations[name] = value
                continue
                
            try:
                name, params = item.name, item.params
            except AttributeError:
                pass
            else:
                mixin = self.get_mixin(name, params)
                
                mixin_declarations = mixin.get_declarations()
            
                for declaration in mixin_declarations:
                    declarations[declaration] = mixin_declarations[declaration]

        return declarations
        
    def get_imports(self):
        try:
            imports = self.parent.get_imports()
        except AttributeError:
            imports = dict()
            
        for item in self.items:
            try:
                target, url = item.target, item.url
            except AttributeError:
                pass
            else:
                try:
                    targets = imports[url]
                except KeyError:
                    targets = list()
                    imports[url] = targets
                
                for media in target:
                    if media not in targets:
                        targets.append(media)
                        
        return imports
        
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
        
    def get_mixin(self, name, params):
        for item in self.items:
            if hasattr(item, 'params') and item.name == name and item.contents:
                return item
                
        for item in self.items:
            try:
                names = item.names
            except AttributeError:
                pass
            else:
                if name in names:
                    return item
        
        try:
            return self.parent.get_mixin(name, params)
        except AttributeError:
            raise AssertionError('mixin %s could not be found' % name)

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

                    declarations = self.get_declarations()

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
