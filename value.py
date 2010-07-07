#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re


VALUE = re.compile('''
        (?P<add>
            \+
        )
    |
        (?P<colour>
            \#
            [0-9]{3,6}
        )
    |
        (?P<colour_name> AliceBlue | AntiqueWhite | Aqua | Aquamarine | Azure |
                         Beige | Bisque | Black | BlanchedAlmond | Blue |
                         BlueViolet | Brown | BurlyWood | CadetBlue | Chartreuse
                         | Chocolate | Coral | CornflowerBlue | Cornsilk |
                         Crimson | Cyan | DarkBlue | DarkCyan | DarkGoldenRod |
                         DarkGray | DarkGreen | DarkKhaki | DarkMagenta |
                         DarkOliveGreen | Darkorange | DarkOrchid | DarkRed
                         | DarkSalmon | DarkSeaGreen | DarkSlateBlue |
                         DarkSlateGray | DarkTurquoise | DarkViolet | DeepPink
                         | DeepSkyBlue | DimGray | DodgerBlue | FireBrick |
                         FloralWhite | ForestGreen | Fuchsia | Gainsboro |
                         GhostWhite | Gold | GoldenRod | Gray | Green |
                         GreenYellow | HoneyDew | HotPink | IndianRed | Indigo |
                         Ivory | Khaki | Lavender | LavenderBlush | LawnGreen |
                         LemonChiffon | LightBlue | LightCoral | LightCyan |
                         LightGoldenRodYellow | LightGrey | LightGreen |
                         LightPink | LightSalmon | LightSeaGreen | LightSkyBlue
                         | LightSlateGray | LightSteelBlue | LightYellow | Lime
                         | LimeGreen | Linen | Magenta | Maroon |
                         MediumAquaMarine | MediumBlue | MediumOrchid |
                         MediumPurple | MediumSeaGreen | MediumSlateBlue |
                         MediumSpringGreen | MediumTurquoise | MediumVioletRed |
                         MidnightBlue | MintCream | MistyRose | Moccasin |
                         NavajoWhite | Navy | OldLace | Olive | OliveDrab |
                         Orange | OrangeRed | Orchid | PaleGoldenRod | PaleGreen
                         | PaleTurquoise | PaleVioletRed | PapayaWhip |
                         PeachPuff | Peru | Pink | Plum | PowderBlue | Purple |
                         Red | RosyBrown | RoyalBlue | SaddleBrown | Salmon |
                         SandyBrown | SeaGreen | SeaShell | Sienna | Silver |
                         SkyBlue | SlateBlue | SlateGray | Snow | SpringGreen |
                         SteelBlue | Tan | Teal | Thistle | Tomato | Turquoise |
                         Violet | Wheat | White | WhiteSmoke | Yellow |
                         YellowGreen )
    |
        (?P<comma>
            ,
        )
    |
        (?P<constant>
            @
            [a-z0-9\-_]*
            [a-z0-9_]+
        )
    |
        (?P<divide>
            \\
        )
    |
        (?P<format>
            format\(
                .+?
            \)
        )
    |
        (?P<local>
            local\(
                .+?
            \)
        )
    |
        (?P<multiply>
            \*
        )
    |
        (?P<number>
            [0-9]+
            
            (?P<unit>
                %                       # percentage
            |
                in                      # inch
            |
                cm                      # centimeter
            |
                mm                      # millimeter
            |
                em                      # 1em is equal to the current font size.
                                        # 2em means 2 times the size of the
                                        # current font. E.g., if an element is
                                        # displayed with a font of 12 pt, then
                                        # '2em' is 24 pt. The 'em' is a very
                                        # useful unit in CSS, since it can adapt
                                        # automatically to the font that the
                                        # reader uses
            |
                ex                      # one ex is the x-height of a font
                                        # (x-height is usually about half the
                                        # font-size)
            |
                pt                      # point (1 pt is the same as 1/72 inch)
            |
                pc                      # pica (1 pc is the same as 12 points)
            |
                px                      # pixels (a dot on the computer screen)
            )?
        )
    |
        (?P<url>
            url\(
                .+?
            \)
        )
    |
        (?P<subtract>
            -
        )
    |
        (?P<string>
            [a-z]+
        |
            '.*?(?!\\\\)'
        |
            ".*?(?!\\\\)"
        )
    |
        (?P<whitespace>
            \s+
        )
''', re.DOTALL | re.IGNORECASE | re.VERBOSE)


GROUPS = ('add', 'colour', 'colour_name', 'comma', 'constant', 'divide',
          'format', 'local', 'multiply', 'number', 'string', 'subtract', 'url',
          'whitespace')


def get_matched_value(match):
    for group_name in GROUPS:
        grouped = match.group(group_name)
        
        if grouped:
            return group_name, grouped
    else:
        raise AssertionError('Unable to find matched group')


def get_value(less, constants):
    parsed = parse_value(less, constants)
    
    value = ''
    
    for item in parsed:
        if value and item['type'] != 'comma':
            value += ' '
        
        value += item['value']
    
    return value
    
    
def parse_value(less, constants):
    parsed = list()

    while less:
        match = VALUE.match(less)
        
        if not match:
            raise ValueError(less)
        
        group_name, grouped = get_matched_value(match)
        
        length = len(grouped)
        
        less = less[length:]
        
        if group_name == 'constant':
            value = constants[grouped]
        elif group_name == 'whitespace':
            continue
        else:
            value = grouped
            
        parsed.append({'type': group_name, 'value': value})

    return parsed