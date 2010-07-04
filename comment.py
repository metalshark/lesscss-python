import re
from node import Node


COMMENT = re.compile('''
    /\*
    
    (?P<comment>
        .*?
    )

    \*/
''', re.DOTALL | re.VERBOSE)


LESS_COMMENT = re.compile(r'''
    //
    
    (?P<comment>
        .*?
    )
    
    (
        \n
    |
        $
    )
''', re.VERBOSE)


def parse_comment(less, parent, **kwargs):
    match = COMMENT.match(less)
    
    if not match:
        match = LESS_COMMENT.match(less)
    
    if not match:
        raise ValueError()
    
    code = match.group()
    comment = match.group('comment')
    
    return Comment(code=code, comment=comment, parent=parent)


class Comment(Node):
    
    __slots__ = ('__comment',)
    
    def __init__(self, code, comment, parent):
        Node.__init__(self, code=code, parent=parent)
        
        self.__comment = comment
        
    def __get_comment(self):
        return self.__comment
        
    comment = property(fget=__get_comment)