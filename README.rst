===============
    xvfbwrapper
===============

Python wrapper for running a display inside X virtual framebuffer (Xvfb)

* Dev: https://github.com/cgoldberg/xvfbwrapper
* PyPI: http://pypi.python.org/pypi/xvfbwrapper

Corey Goldberg - 2012, 2013

****

*********
    Setup
*********

Install xvfbwrapper from PyPI::
    
    pip install xvfbwrapper

***********************
    System Requirements
***********************

* Xvfb (`sudo apt-get install xvfb`, or similar)
* Python 2.7 or 3.2+ (tested on py27, py32, py33)

**************************************
    About Xvfb (X Virtual Framebuffer)
**************************************

In the X Window System, Xvfb or X Virtual FrameBuffer is an X11 server that performs all graphical operations in memory, not showing any screen output. This virtual server does not require the computer it is running on to even have a screen or any input device. Only a network layer is necessary.

************************
    Example: Basic Usage
************************

::
    
    from xvfbwrapper import Xvfb
    
    vdisplay = Xvfb()
    vdisplay.start()
    
    # launch stuff inside virtual display here

    vdisplay.stop()

***************************************
    Example: Usage as a Context Manager
***************************************

::
    
    from xvfbwrapper import Xvfb
    
    with Xvfb() as xvfb:
        # launch stuff inside virtual display here.
        # It starts/stops in this code block.


**********************************************
    Example: Headless Selenium WebDriver Tests
**********************************************

::

    from selenium import webdriver
    from xvfbwrapper import Xvfb

    import unittest


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

This code uses `selenium` and `xvfbwrapper` to run a test with Firefox inside a headless display.

* install selenium bindings: `pip install selenium`
* Firefox will launch inside virtual display (headless)
* browser is not shown while tests are run
