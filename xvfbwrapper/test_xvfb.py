#!/usr/bin/env python


from xvfbwrapper import Xvfb

import os
import unittest


class TestXvfb(unittest.TestCase):
    
    def test_start(self):
        xvfb = Xvfb()
        self.addCleanup(xvfb.stop)
        xvfb.start()
        self.assertEqual(':%d' % xvfb.vdisplay_num, os.environ['DISPLAY'])
        self.assertIsNot(None, xvfb.proc)

    def test_stop(self):
        orig = os.environ['DISPLAY']
        xvfb = Xvfb()
        xvfb.start()
        self.assertNotEqual(orig, os.environ['DISPLAY'])
        xvfb.stop()
        self.assertEquals(orig, os.environ['DISPLAY'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
