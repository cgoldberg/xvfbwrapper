#!/usr/bin/env python


"""distutils setup/install script for xvfbwrapper"""


import os
import setuptools
import sys


VERSION = '0.2.10.dev'


this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, 'README.rst')) as f:
    LONG_DESCRIPTION = '\n' + f.read()

TESTS_REQUIRE = []
if sys.version_info.major < 3:
    TESTS_REQUIRE.append('mock')


setuptools.setup(
    name='xvfbwrapper',
    version=VERSION,
    py_modules=['xvfbwrapper'],
    author='Corey Goldberg',
    author_email='cgoldberg _at_ gmail.com',
    description='Manage headless displays with Xvfb (X virtual framebuffer)',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/cgoldberg/xvfbwrapper',
    download_url='https://pypi.python.org/pypi/xvfbwrapper',
    tests_require=TESTS_REQUIRE,
    keywords='xvfb headless virtual display x11 testing'.split(),
    license='MIT',
    classifiers=[
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
