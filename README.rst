===============
    xvfbwrapper
===============


**Manage headless displays with Xvfb (X virtual framebuffer)**

----

---------
    Info:
---------

- Development: https://github.com/cgoldberg/xvfbwrapper
- Releases: https://pypi.org/project/xvfbwrapper
- Author: `Corey Goldberg <https://github.com/cgoldberg>`_ - 2012-2025
- License: MIT

----

----------------------
    About xvfbwrapper:
----------------------

`xvfbwrapper` is a python module for controlling virtual displays with Xvfb.

----

------------------
    What is Xvfb?:
------------------

`Xvfb` (X virtual framebuffer) is a display server implementing the X11 display server protocol.
It runs in memory and does not require a physical display or input devices. Only a network layer is necessary.

`Xvfb` is useful for running acceptance tests on headless servers.

----

----------------------------------
    Install xvfbwrapper from PyPI:
----------------------------------

.. code:: bash

    pip install xvfbwrapper

----

------------------------
    System Requirements:
------------------------

* Python 3.8+
* X Window System
* Xvfb (`sudo apt-get install xvfb`, `yum install xorg-x11-server-Xvfb`, etc)
* File locking with `fcntl` 

----

-------------
    Examples:
-------------

****************
    Basic Usage:
****************

.. code:: python

    from xvfbwrapper import Xvfb

    vdisplay = Xvfb()
    vdisplay.start()

    try:
        # launch stuff inside virtual display here.
    finally:
        # always either wrap your usage of Xvfb() with try / finally,
        # or alternatively use Xvfb as a context manager.
        # If you don't, you'll probably end up with a bunch of junk in /tmp
        vdisplay.stop()

----

*********************************************
    Basic Usage, specifying display geometry:
*********************************************

.. code:: python

    from xvfbwrapper import Xvfb

    vdisplay = Xvfb(width=1280, height=740)
    vdisplay.start()

    try:
        # launch stuff inside virtual display here.
    finally:
        vdisplay.stop()

----

*******************************************
    Basic Usage, specifying display number:
*******************************************

.. code:: python

    from xvfbwrapper import Xvfb

    vdisplay = Xvfb(display=23)
    vdisplay.start()
    # Xvfb is started with display :23
    # see vdisplay.new_display

----

*******************************
    Usage as a Context Manager:
*******************************

.. code:: python

    from xvfbwrapper import Xvfb

    with Xvfb() as xvfb:
        # launch stuff inside virtual display here.
        # Xvfb will stop when this block completes

----

********************************************************
    Usage in Testing: Headless Selenium WebDriver Tests:
********************************************************

This test class uses *selenium webdriver* and *xvfbwrapper* to run tests
on Chrome with a headless display.

.. code:: python

    import unittest

    from selenium import webdriver
    from xvfbwrapper import Xvfb


    class TestPages(unittest.TestCase):

        def setUp(self):
            self.xvfb = Xvfb(width=1280, height=720)
            self.addCleanup(self.xvfb.stop)
            self.xvfb.start()
            self.browser = webdriver.Chrome()
            self.addCleanup(self.browser.quit)

        def testUbuntuHomepage(self):
            self.browser.get('https://www.ubuntu.com')
            self.assertIn('Ubuntu', self.browser.title)

        def testGoogleHomepage(self):
            self.browser.get('https://www.google.com')
            self.assertIn('Google', self.browser.title)


    if __name__ == '__main__':
        unittest.main()

* virtual display is launched
* Chrome launches inside virtual display (headless)
* browser is not shown while tests are run
* conditions are asserted in each test case
* browser quits during cleanup
* virtual display stops during cleanup

*Look Ma', no browser!*

(You can also take screenshots inside the virtual display to help diagnose test failures)

----

***************************************
    Usage with multi-threaded execution
***************************************

To run several xvfb servers at the same time, you can use the environ keyword
when starting the Xvfb instances. This provides isolation between threads. Be
sure to use the environment dictionary you initialize Xvfb with in your
subsequent system calls. Also, if you wish to inherit your current environment
you must use the copy method of os.environ and not simply assign a new
variable to os.environ:

.. code:: python

    from xvfbwrapper import Xvfb
    import subprocess as sp
    import os

    isolated_environment = os.environ.copy()
    xvfb = Xvfb(environ=isolated_environment)
    xvfb.start()
    sp.run(
        "xterm & sleep 1; kill %1 ",
        shell=True,
        env=isolated_environment,
    )
    xvfb.stop()

----

----------------------------------------------------
    xvfbwrapper Development: running the unit tests:
----------------------------------------------------

To create a virtual env and install required testing libraries:

.. code:: bash

    $ python -m venv venv
    $ source ./venv/bin/activate
    (venv)$ pip install -r requirements_test.txt

To run all tests, linting, and type checking across all
supported/installed Python environments:

.. code:: bash

    (venv)$ tox

To run all tests in the default Python environment:

.. code:: bash

    (venv)$ pytest
