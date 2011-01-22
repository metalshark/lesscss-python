# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

Copyright (c) 2011 Evgeny V. Generalov. 
mailto:e.generalov@gmail.com
"""
import sys
import locale


class Writer(object):
    """text writer"""

    def __init__(self, output=None, out_encoding=None):
        self.out = None
        self.out_encoding = out_encoding
        self.set_output(output)

    def set_output(self, output=None):
        """set output stream"""
        self.out = output or sys.stdout

    def write(self, string):
        """write a string to the output"""
        self.out.write(self._encode(string))

    def writeln(self, string):
        """write a line to the output"""
        print >> self.out, self._encode(string)

    def _encode(self, data):
        """encode data to string"""
        # py3k streams handle their encoding :
        if sys.version_info >= (3, 0):
            return data
        if not isinstance(data, unicode):
            return data
        # data is string
        encoding = (self.out_encoding or
                    getattr(self.out, 'encoding', None) or
                    locale.getdefaultlocale()[1] or
                    sys.getdefaultencoding())
        return data.encode(encoding)

