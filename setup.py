#!/usr/bin/env python


""" setup/install script for xvfbwrapper """


from distutils.core import setup

import xvfbwrapper


with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()


setup(
        name = 'xvfbwrapper',
        version = xvfbwrapper.__version__,
        packages = ['xvfbwrapper'],
        author = 'Corey Goldberg',
        author_email = 'corey@goldb.org',
        maintainer = 'Corey Goldberg',
        maintainer_email = 'corey@goldb.org',
        description = 'wrapper for running display inside X virtual framebuffer (Xvfb)',
        long_description = LONG_DESCRIPTION,
        url = 'https://github.com/cgoldberg/xvfbwrapper',
        download_url = 'http://pypi.python.org/pypi/xvfbwrapper',
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
