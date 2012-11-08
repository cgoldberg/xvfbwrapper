from xvfbwrapper import Xvfb

import unittest
from selenium import webdriver


class TestUbuntuHomepage(unittest.TestCase):
    def setUp(self):
        self.vdisplay = Xvfb(width=1280, height=720)
        self.vdisplay.start()
        self.browser = webdriver.Firefox()
        
    def testTitle(self):
        self.browser.get('http://www.ubuntu.com')
        self.assertIn('Ubuntu', self.browser.title)
        
    def tearDown(self):
        self.browser.quit()
        self.vdisplay.stop()


if __name__ == '__main__':
    unittest.main(verbosity=2)
