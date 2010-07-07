#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re


COLOURS = {'aliceblue':            '#f0f8ff', 'antiquewhite':         '#faebd7',
           'aqua':                 '#00ffff', 'aquamarine':           '#7fffd4',
           'azure':                '#f0ffff', 'beige':                '#f5f5dc',
           'bisque':               '#ffe4c4', 'black':                '#000000',
           'blanchedalmond':       '#ffebcd', 'blue':                 '#0000ff',
           'blueviolet':           '#8a2be2', 'brown':                '#a52a2a',
           'burlywood':            '#deb887', 'cadetblue':            '#5f9ea0',
           'chartreuse':           '#7fff00', 'chocolate':            '#d2691e',
           'coral':                '#ff7f50', 'cornflowerblue':       '#6495ed',
           'cornsilk':             '#fff8dc', 'crimson':              '#dc143c',
           'cyan':                 '#00ffff', 'darkblue':             '#00008b',
           'darkcyan':             '#008b8b', 'darkgoldenrod':        '#b8860b',
           'darkgray':             '#a9a9a9', 'darkgreen':            '#006400',
           'darkkhaki':            '#bdb76b', 'darkmagenta':          '#8b008b',
           'darkolivegreen':       '#556b2f', 'darkorange':           '#ff8c00',
           'darkorchid':           '#9932cc', 'darkred':              '#8b0000',
           'darksalmon':           '#e9967a', 'darkseagreen':         '#8fbc8f',
           'darkslateblue':        '#483d8b', 'darkslategray':        '#2f4f4f',
           'darkturquoise':        '#00ced1', 'darkviolet':           '#9400d3',
           'deeppink':             '#ff1493', 'deepskyblue':          '#00bfff',
           'dimgray':              '#696969', 'dodgerblue':           '#1e90ff',
           'firebrick':            '#b22222', 'floralwhite':          '#fffaf0',
           'forestgreen':          '#228b22', 'fuchsia':              '#ff00ff',
           'gainsboro':            '#dcdcdc', 'ghostwhite':           '#f8f8ff',
           'gold':                 '#ffd700', 'goldenrod':            '#daa520',
           'gray':                 '#808080', 'green':                '#008000',
           'greenyellow':          '#adff2f', 'honeydew':             '#f0fff0',
           'hotpink':              '#ff69b4', 'indianred ':           '#cd5c5c',
           'indigo ':              '#4b0082', 'ivory':                '#fffff0',
           'khaki':                '#f0e68c', 'lavender':             '#e6e6fa',
           'lavenderblush':        '#fff0f5', 'lawngreen':            '#7cfc00',
           'lemonchiffon':         '#fffacd', 'lightblue':            '#add8e6',
           'lightcoral':           '#f08080', 'lightcyan':            '#e0ffff',
           'lightgoldenrodyellow': '#fafad2', 'lightgrey':            '#d3d3d3',
           'lightgreen':           '#90ee90', 'lightpink':            '#ffb6c1',
           'lightsalmon':          '#ffa07a', 'lightseagreen':        '#20b2aa',
           'lightskyblue':         '#87cefa', 'lightslategray':       '#778899',
           'lightsteelblue':       '#b0c4de', 'lightyellow':          '#ffffe0',
           'lime':                 '#00ff00', 'limegreen':            '#32cd32',
           'linen':                '#faf0e6', 'magenta':              '#ff00ff',
           'maroon':               '#800000', 'mediumaquamarine':     '#66cdaa',
           'mediumblue':           '#0000cd', 'mediumorchid':         '#ba55d3',
           'mediumpurple':         '#9370d8', 'mediumseagreen':       '#3cb371',
           'mediumslateblue':      '#7b68ee', 'mediumspringgreen':    '#00fa9a',
           'mediumturquoise':      '#48d1cc', 'mediumvioletred':      '#c71585',
           'midnightblue':         '#191970', 'mintcream':            '#f5fffa',
           'mistyrose':            '#ffe4e1', 'moccasin':             '#ffe4b5',
           'navajowhite':          '#ffdead', 'navy':                 '#000080',
           'oldlace':              '#fdf5e6', 'olive':                '#808000',
           'olivedrab':            '#6b8e23', 'orange':               '#ffa500',
           'orangered':            '#ff4500', 'orchid':               '#da70d6',
           'palegoldenrod':        '#eee8aa', 'palegreen':            '#98fb98',
           'paleturquoise':        '#afeeee', 'palevioletred':        '#d87093',
           'papayawhip':           '#ffefd5', 'peachpuff':            '#ffdab9',
           'peru':                 '#cd853f', 'pink':                 '#ffc0cb',
           'plum':                 '#dda0dd', 'powderblue':           '#b0e0e6',
           'purple':               '#800080', 'red':                  '#ff0000',
           'rosybrown':            '#bc8f8f', 'royalblue':            '#4169e1',
           'saddlebrown':          '#8b4513', 'salmon':               '#fa8072',
           'sandybrown':           '#f4a460', 'seagreen':             '#2e8b57',
           'seashell':             '#fff5ee', 'sienna':               '#a0522d',
           'silver':               '#c0c0c0', 'skyblue':              '#87ceeb',
           'slateblue':            '#6a5acd', 'slategray':            '#708090',
           'snow':                 '#fffafa', 'springgreen':          '#00ff7f',
           'steelblue':            '#4682b4', 'tan':                  '#d2b48c',
           'teal':                 '#008080', 'thistle':              '#d8bfd8',
           'tomato':               '#ff6347', 'turquoise':            '#40e0d0',
           'violet':               '#ee82ee', 'wheat':                '#f5deb3',
           'white':                '#ffffff', 'whitesmoke':           '#f5f5f5',
           'yellow':               '#ffff00', 'yellowgreen':          '#9acd32'}


VALUE = re.compile('''
        (?P<add>
            \+
        )
    |
        (?P<colour>
            \#
            [0-9A-F]{6}
        )
    |
        (?P<short_colour>
            \#
            [0-9A-F]{3}
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
            /
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
          'format', 'local', 'multiply', 'number', 'short_colour', 'string',
          'subtract', 'url', 'whitespace')
          
          
def add(arg1, arg2):
    if arg1['type'] == 'colour' and arg2['type'] == 'colour':
        colour1_red, colour1_green, colour1_blue = get_rgb(arg1['value'])
        colour2_red, colour2_green, colour2_blue = get_rgb(arg2['value'])
        
        red   = colour1_red   + colour2_red
        green = colour1_green + colour2_green
        blue  = colour1_blue  + colour2_blue
        
        return get_colour_value(red, green, blue)
    elif arg1['type'] == 'number' and arg2['type'] == 'number':
        num1 = int(arg1['value'])
        num2 = int(arg2['value'])
        
        return str(num1 + num2)
    else:
        raise ValueError('%s cannot be added to %s' %
                         (arg1['type'], arg2['type']))
          
          
def divide(arg1, arg2):
    if arg1['type'] == 'colour' and arg2['type'] == 'number':
        operand = int(arg2['value'])
        
        if operand == 0:
            raise ZeroDivisionError()
    
        colour1_red, colour1_green, colour1_blue = get_rgb(arg1['value'])
        
        red   = colour1_red   / operand
        green = colour1_green / operand
        blue  = colour1_blue  / operand
        
        return get_colour_value(red, green, blue)
        
    else:
        raise ValueError('%s cannot be divided by %s' %
                         (arg1['type'], arg2['type']))

                         
def get_colour(value):
    value = value.lower()

    for colour in COLOURS:
        if value == COLOURS[colour]:
            return colour
            
    if value[1:4] == value[4:7]:
        return value[0:4]
    
    return value
    
    
def get_colour_value(red, green, blue):
    hex_red   = hex(normalise_colour(red))
    hex_green = hex(normalise_colour(green))
    hex_blue  = hex(normalise_colour(blue))
    
    return '#%s%s%s' % (hex_red[2:], hex_green[2:], hex_blue[2:])

    
def get_matched_value(match):
    for group_name in GROUPS:
        grouped = match.group(group_name)
        
        if grouped:
            return group_name, grouped
    else:
        raise AssertionError('Unable to find matched group')
        
        
def get_rgb(colour):
    red   = int(colour[1:3], 16)
    green = int(colour[3:5], 16)
    blue  = int(colour[5:7], 16)
    
    return red, green, blue


def get_value(less, constants):
    parsed = parse_value(less, constants)
    
    value = ''
    
    i = 0
    
    length = len(parsed)
    
    while i != length:
        item = parsed[i]
    
        if value and item['type'] != 'comma':
            value += ' '
        
        if i != length - 1 \
        and parsed[i + 1]['type'] in ('add', 'divide', 'multiply', 'subtract'):
            operator = parsed[i + 1]['type']            
            
            if operator == 'add':
                this_value = add(parsed[i], parsed[i + 2])
            elif operator == 'divide':
                this_value = divide(parsed[i], parsed[i + 2])
            elif operator == 'multiply':
                this_value = multiply(parsed[i], parsed[i + 2])
            elif operator == 'subtract':
                this_value = subtract(parsed[i], parsed[i + 2])
        
            i += 2
        else:
            this_value = item['value']
            
        if item['type'] == 'colour':
            this_value = get_colour(this_value)
            
        value += this_value
        
        i += 1
    
    return value
          
          
def multiply(arg1, arg2):
    if arg1['type'] == 'colour' and arg2['type'] == 'number':
        operand = int(arg2['value'])
    
        colour1_red, colour1_green, colour1_blue = get_rgb(arg1['value'])
        
        red   = colour1_red   * operand
        green = colour1_green * operand
        blue  = colour1_blue  * operand
        
        return get_colour_value(red, green, blue)
        
    else:
        raise ValueError('%s cannot be multiplied by %s' %
                         (arg1['type'], arg2['type']))
        
        
def normalise_colour(colour):
    if colour < 0:
        return 0
    elif colour > 255:
        return 255
    else:
        return colour
    
    
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
            constant = constants[grouped]
            
            value = ''
            
            while value != grouped:
                grouped = value
                
                value = get_value(constant, constants)
                
            group_name, value = get_matched_value(VALUE.match(grouped))
        
        if group_name == 'colour_name':
            group_name = 'colour'
            value = COLOURS[grouped.lower()]
        elif group_name == 'short_colour':
            group_name = 'colour'
            half = grouped[1:]
            value = '#%s%s' % (half, half)
        elif group_name == 'whitespace':
            continue
        else:
            value = grouped
            
        parsed.append({'type': group_name, 'value': value})

    return parsed
          
          
def subtract(arg1, arg2):
    if arg1['type'] == 'colour' and arg2['type'] == 'colour':
        colour1_red, colour1_green, colour1_blue = get_rgb(arg1['value'])
        colour2_red, colour2_green, colour2_blue = get_rgb(arg2['value'])
        
        red   = colour1_red   - colour2_red
        green = colour1_green - colour2_green
        blue  = colour1_blue  - colour2_blue
        
        return get_colour_value(red, green, blue)
        
    else:
        raise ValueError('%s cannot be subtracted from %s' %
                         (arg1['type'], arg2['type']))
