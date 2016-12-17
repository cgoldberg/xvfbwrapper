#!/usr/bin/env python


"""distutils setup/install script for xvfbwrapper"""


import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, 'README.rst')) as f:
    LONG_DESCRIPTION = '\n' + f.read()

tests_require = []
try:
    from unittest import mock  # noqa
except ImportError:
    tests_require.append('mock')

setup(
    name='xvfbwrapper',
    version='0.2.9',
    py_modules=['xvfbwrapper'],
    author='Corey Goldberg',
    author_email='cgoldberg _at_ gmail.com',
    description='run headless display inside X virtual framebuffer (Xvfb)',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/cgoldberg/xvfbwrapper',
    download_url='http://pypi.python.org/pypi/xvfbwrapper',
    tests_require=tests_require,
    keywords='xvfb virtual display headless x11'.split(),
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
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
