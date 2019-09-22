===============
    xvfbwrapper
===============


**Manage headless displays with Xvfb (X virtual framebuffer)**

.. image:: https://travis-ci.org/cgoldberg/xvfbwrapper.svg?branch=master
    :target: https://travis-ci.org/cgoldberg/xvfbwrapper

----

---------
    Info:
---------

- Dev: https://github.com/cgoldberg/xvfbwrapper
- Releases: https://pypi.org/project/xvfbwrapper/
- Author: `Corey Goldberg <https://github.com/cgoldberg>`_ - 2012-2019
- License: MIT

----

----------------------
    About xvfbwrapper:
----------------------

xvfbwrapper is a python module for controlling virtual displays with Xvfb.

----

------------------
    What is Xvfb?:
------------------

Xvfb (X virtual framebuffer) is a display server implementing the X11 display server protocol. It runs in memory and does not require a physical display.  Only a network layer is necessary.

Xvfb is useful for running acceptance tests on headless servers.

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

* X11 Windowing System
* Xvfb (`sudo apt-get install xvfb`, `yum install xorg-x11-server-Xvfb`, etc)
* Python 2.7 or 3.4+

----

++++++++++++
    Examples
++++++++++++

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

*******************************************************
    Testing Example: Headless Selenium WebDriver Tests:
*******************************************************

This test class uses *selenium webdriver* and *xvfbwrapper* to run test cases on Firefox with a headless display.

.. code:: python

    import unittest

    from selenium import webdriver
    from xvfbwrapper import Xvfb


    class TestPages(unittest.TestCase):

        def setUp(self):
            self.xvfb = Xvfb(width=1280, height=720)
            self.addCleanup(self.xvfb.stop)
            self.xvfb.start()
            self.browser = webdriver.Firefox()
            self.addCleanup(self.browser.quit)

        def testUbuntuHomepage(self):
            self.browser.get('http://www.ubuntu.com')
            self.assertIn('Ubuntu', self.browser.title)

        def testGoogleHomepage(self):
            self.browser.get('http://www.google.com')
            self.assertIn('Google', self.browser.title)


    if __name__ == '__main__':
        unittest.main()

* virtual display is launched
* Firefox launches inside virtual display (headless)
* browser is not shown while tests are run
* conditions are asserted in each test case
* browser quits during cleanup
* virtual display stops during cleanup

*Look Ma', no browser!*

(You can also take screenshots inside the virtual display to help diagnose test failures)
