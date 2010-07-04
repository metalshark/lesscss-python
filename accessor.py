import re
from node import Node


ACCESSOR = re.compile('''
    (?P<value>
        [a-z 0-9 \- _ \* \. \s , : # &]+?
        (
            \s*
            >
            
            \s*
            [a-z 0-9 \- _ \* \. \s , : # &]+?
        )+
    |
        [a-z 0-9 \- _ \* \. \s , : # &]+?
        \[
            .+?
        \]
    )
    
    \s*
    
    (
        ;
    |
        }
    )
''', re.DOTALL | re.VERBOSE)


def parse_accessor(less, parent=None, **kwargs):
    match = ACCESSOR.match(less)
    
    if not match:
        raise ValueError()
    
    code = match.group()
    accessor = match.group('value')
    
    return Accessor(accessor=accessor, code=code, parent=parent)


class Accessor(Node):
    
    __slots__ = ('__accessor',)
    
    def __init__(self, accessor, code, parent):
        Node.__init__(self, code=code, parent=parent)
        
        self.__accessor = accessor
        
    def __get_accessor(self):
        return self.__accessor
        
    accessor = property(fget=__get_accessor)