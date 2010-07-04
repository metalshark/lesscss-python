import re
from node import Node
from property import Property


CONSTANT = re.compile('''
    (?P<name>
        @
        [a-z0-9\-_]+
    )
    
    \s*
    
    :
    
    \s*
    
    (?P<value>
        .+?
    )
    
    \s*
    
    ;
''', re.VERBOSE)


def parse_constant(less, parent, **kwargs):
    match = CONSTANT.match(less)
    
    if not match:
        raise ValueError()
        
    code = match.group()
    name = match.group('name')
    value = match.group('value')
    
    return Constant(code=code, name=name, parent=parent, value=value)
    
    
class Constant(Property):
    pass
