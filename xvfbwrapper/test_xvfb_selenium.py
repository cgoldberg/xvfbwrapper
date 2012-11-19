#!/usr/bin/env python

from selenium import webdriver
from xvfbwrapper import Xvfb

import unittest


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
