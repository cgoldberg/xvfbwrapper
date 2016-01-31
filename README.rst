===============
    xvfbwrapper
===============


**Python wrapper for running a display inside X virtual framebuffer (Xvfb).**

.. image:: https://travis-ci.org/cgoldberg/xvfbwrapper.svg?branch=master
    :target: https://travis-ci.org/cgoldberg/xvfbwrapper

----

---------
    Info:
---------

- Dev Home (GitHub): https://github.com/cgoldberg/xvfbwrapper
- Releases (PyPI): https://pypi.python.org/pypi/xvfbwrapper
- Author: `Corey Goldberg <https://github.com/cgoldberg/xvfbwrapper>`_ - 2012, 2013, 2015, 2016
- License: MIT

----

---------------
    About Xvfb:
---------------

You may want to run a program that uses a graphical display, requiring X11 and a physical display attached.  However, With Xvfb you can run headless inside a virtual dislpay.  In the X Window System, Xvfb or "X Virtual FrameBuffer" is an X11 server that performs all graphical operations in memory, not showing any screen output. This virtual server does not require the computer it is running on to even have a screen or any input device. Only a network layer is necessary.

Xvfb is often used for running browser-based acceptance tests on a headless server.

----

----------------------
    About xvfbwrapper:
----------------------

xvfbwrapper is a small python wrapper for controlling Xvfb.  It works nicely when Integrating wiith python test suites or other Python code.

----

----------------------------------
    Install xvfbwrapper from PyPI:
----------------------------------

  ``pip install xvfbwrapper``

----

------------------------
    System Requirements:
------------------------

* Xvfb (``sudo apt-get install xvfb``, or similar)
* Python 2.7 or 3.2+ (tested on py27, py32, py33, py34, 3.5, pypy)

----

++++++++++++
    Examples
++++++++++++

****************
    Basic Usage:
****************

::

    from xvfbwrapper import Xvfb

    vdisplay = Xvfb()
    vdisplay.start()

    # launch stuff inside
    # virtual display here.

    vdisplay.stop()

----

*************************************************************
    Basic Usage, specifying display geometry and color depth:
*************************************************************

::

    from xvfbwrapper import Xvfb

    vdisplay = Xvfb(width=1280, height=740, colordepth=16)
    vdisplay.start()

    # launch stuff inside
    # virtual display here.

    vdisplay.stop()

----

*******************************
    Usage as a Context Manager:
*******************************

::

    from xvfbwrapper import Xvfb

    with Xvfb() as xvfb:
        # launch stuff inside virtual display here.
        # It starts/stops around this code block.

----

*******************************************************
    Testing Example: Headless Selenium WebDriver Tests:
*******************************************************

::

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
        unittest.main(verbosity=2)


This above code uses `selenium` and `xvfbwrapper` to run a test with Firefox inside a headless display.

It will:

* install selenium bindings: `pip install selenium`
* Firefox will launch inside virtual display (headless)
* browser is not shown while tests are run

*Look Ma', no browser!*
