===============
    xvfbwrapper
===============

Python wrapper for running display inside X virtual framebuffer (Xvfb)

Home: http://pypi.python.org/pypi/xvfbwrapper
Dev: https://github.com/cgoldberg/xvfbwrapper

* `Selenium Project Home <http://selenium.googlecode.com>`_

----

*********************************
    Install xvfbwrapper from PyPI
*********************************

::
    
    pip install xvfbwrapper


**************************************
    About Xvfb (X Virtual Framebuffer)
**************************************

In the X Window System, Xvfb or X virtual framebuffer is an X11 server that performs all graphical operations in memory, not showing any screen output. This virtual server does not require the computer it is running on to even have a screen or any input device. Only a network layer is necessary.

***********************
    System Requirements
***********************

  * Xvfb ('sudo apt-get install xvfb' or similar)
  * Python 2

************************
    Example: Basic Usage
************************

::
    
    from xvfbwrapper import Xvfb

    vdisplay = Xvfb()
    vdisplay.start()
    
    # launch stuff inside virtual display here

    vdisplay.stop()

****************************************************
    Example: Headless Selenium WebDriver and Firefox
****************************************************
  * install selenium bindings: `pip install selenium`
  * Firefox will launch inside virtual display (headless)
  * browser is not shown while test is run

::

    from xvfbwrapper import Xvfb

    import unittest
    from selenium import webdriver


    class TestHomepages(unittest.TestCase):
        def setUp(self):
            self.vdisplay = Xvfb(width=1280, height=720)
            self.vdisplay.start()
            self.browser = webdriver.Firefox()
            
        def testUbuntuHomepage(self):
            self.browser.get('http://www.ubuntu.com')
            self.assertIn('Ubuntu', self.browser.title)
            
        def testGoogleHomepage(self):
            self.browser.get('http://www.google.com')
            self.assertIn('Google', self.browser.title)
            
        def tearDown(self):
            self.browser.quit()
            self.vdisplay.stop()


    if __name__ == '__main__':
        unittest.main(verbosity=2)

----

