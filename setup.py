#!/usr/bin/env python


"""distutils setup/install script for xvfbwrapper"""


import os
import setuptools
import sys


this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, 'README.rst')) as f:
    LONG_DESCRIPTION = '\n' + f.read()

if sys.version_info.major < 3:
    tests_require = ['mock']
else:
    tests_require = []


setuptools.setup(
    name='xvfbwrapper',
    version='0.2.10dev-b',
    py_modules=['xvfbwrapper'],
    author='Corey Goldberg',
    author_email='cgoldberg _at_ gmail.com',
    description='Manage headless displays with Xvfb (X virtual framebuffer)',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/cgoldberg/xvfbwrapper',
    download_url='https://pypi.python.org/pypi/xvfbwrapper',
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
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
