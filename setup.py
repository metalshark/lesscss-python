#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
This file is part of lesscss-python.

lesscss-python is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

lesscss-python is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with lesscss-python. If not, see <http://www.gnu.org/licenses/>.
'''

import os
from distutils.core import setup
from lesscss import __version__ as version

read = lambda *xs: open(os.path.join(os.path.dirname(__file__), *xs)).read()

setup(
    name = 'lesscss-python',
    description = 'A LessCSS Compiler in Python',
    long_description = read('README.rst'),
    version = version,
    author = 'Beech Horn',
    maintainer = 'Evgeny V. Generalov',
    maintainer_email = 'e.generalov@gmail.com',
    license = 'GPLv3',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords = 'lesscss css stylesheet language',
    packages = ['lesscss'],
    scripts=['lesscss/lessc.py'],
)
