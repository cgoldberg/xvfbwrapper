#!/usr/bin/env python


""" setup/install script for xvfbwrapper """


import os
from distutils.core import setup

import xvfbwrapper


this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, 'README.rst')) as f:
    LONG_DESCRIPTION = '\n' + f.read()


setup(
        name = 'xvfbwrapper',
        version = xvfbwrapper.__version__,
        packages = ['xvfbwrapper'],
        author = 'Corey Goldberg',
        author_email = 'cgoldberg _at_ gmail.com',
        description = 'wrapper for running a display inside X virtual framebuffer (Xvfb)',
        long_description = LONG_DESCRIPTION,
        url = 'http://cgoldberg.github.com/xvfbwrapper/',
        download_url = 'http://pypi.python.org/pypi/xvfbwrapper',
        keywords = 'xvfb virtual display headless x11'.split(),
        license = 'MIT',
        classifiers = [
            'Operating System :: Unix',
            'Operating System :: POSIX :: Linux',
            'Intended Audience :: Developers',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Topic :: Software Development :: Libraries :: Python Modules',
            ]
     )
