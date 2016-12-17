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
- Releases: https://pypi.python.org/pypi/xvfbwrapper
- Author: `Corey Goldberg <https://github.com/cgoldberg>`_ - 2012-2016
- License: MIT

----

----------------------
    About xvfbwrapper:
----------------------

xvfbwrapper is a python wrapper for controlling Xvfb.

----

---------------
    About Xvfb:
---------------

Xvfb (X virtual framebuffer) is a display server implementing the X11 display server protocol. It runs in memory and does not require a physical display.  Only a network layer is necessary.

Xvfb is especially useful for running acceptance tests on headless servers.

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
* Python 2.7 or 3.3+

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

*********************************************
    Basic Usage, specifying display geometry:
*********************************************

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
        unittest.main()


The test class above uses `selenium` and `xvfbwrapper` to run each test case with Firefox inside a headless display.

* virtual display is launched
* Firefox launches inside virtual display (headless)
* browser is not shown while tests are run
* conditions are asserted in each test case
* browser quits during cleanup
* virtual display stops during cleanup

*Look Ma', no browser!*

(You can also take screenshots inside the virtual display for diagnosing test failures)
