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


from lesscss.accessor import parse_accessor
from lesscss.comment  import parse_comment
from lesscss.constant import parse_constant
from lesscss.importer import parse_import
from lesscss.media    import parse_media, Media
from lesscss.mixin    import parse_mixin
from lesscss.property import parse_property
from lesscss.rules    import Rules
from lesscss.selector import parse_selector


PARSERS = (parse_accessor,
           parse_comment,
           parse_constant,
           parse_import,
           parse_media,
           parse_mixin,
           parse_property,
           parse_selector)


def compile(less, path=None):
    css = ''
    
    parsed = Rules(code=less)

    parse(less, path=path, parent=parsed)
        
    return unicode(parsed)


def parse(less, parent, path=None):
    # get rid of whitespace at the end of the less code
    less = less.rstrip()
    
    # keep reading the less code until no more exists
    while less:
    
        # get rid of whitespace before the less code
        less = less.lstrip()
        
        # give all of the parsers a shot at reading the remainder
        for parser in PARSERS:
        
            # parsers will throw a ValueError exception if they fail
            try:
                parsed_item = parser(less, path=path, parent=parent)

            # when the parser fails...
            except ValueError:
            
                # ...try the next one
                pass
            
            # when the parser is successful
            else:
            
                # cache the parsed code
                code = parsed_item.code
            
                # find out how much less code to chop off
                code_length = len(code)
                
                # cache the following code
                following_code = less[:code_length]
                
                # check that it is next
                if following_code != code:
                    raise AssertionError('The following code is "%s" not "%s"' %
                                         (following_code, code))
            
                # remove it
                less = less[code_length:]
                
                # detect imports
                try:
                
                    imported_less = parsed_item.less
                    
                    media = parsed_item.media
                    
                    if media:
                    
                        imported_less = '@media %s {\n%s\n}' % \
                                        (', '.join(media), imported_less)
                
                    if less:
                
                        # add a safety gap
                        less += '\n'
                        
                    less += imported_less
                    
                    # then move on to the rest
                    break
                    
                except AttributeError:
                
                    pass
                
                try:
                
                    # read the contents of the nested rule
                    contents = parsed_item.contents
                    
                    # if there are any contents then parse them
                    if contents:
                    
                        # parse the contents
                        parse(contents, parent=parsed_item, path=path)
                
                except AttributeError:
                
                    pass
                        
                # add the parsed item to its parent
                try:
                    parent.items.append(parsed_item)
                except AttributeError:
                    pass
                
                # then move on to the rest
                break;

        # if all of the parsers fail
        else:
        
            # report an error with the less code
            raise ValueError('Unable to read onwards from: %s' % less)


if __name__ == '__main__':
    import optparse
    import sys
    import traceback

    from lesscss.contrib import console

    usage = "usage: %prog [source [destination]]"
    parser = optparse.OptionParser(usage=usage)
    (options, argv) = parser.parse_args()

    def main(argv):
        source = open(argv[0]) if len(argv) > 0 else sys.stdin
        destination = argv[1] if len(argv) > 1 else sys.stdout
        output = console.Writer(destination)
        output.write(compile(source.read()))

    try:
        main(argv)
    except Exception, e:
        console.Writer(sys.stderr).writeln(
                traceback.format_exc() if __debug__
                else str(e))
        sys.exit(1)

