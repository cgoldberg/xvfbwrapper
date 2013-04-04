#!/usr/bin/env python


from .xvfbwrapper import Xvfb

import os
import unittest


class TestXvfb(unittest.TestCase):
    
    def test_start(self):
        xvfb = Xvfb()
        self.addCleanup(xvfb.stop)
        xvfb.start()
        self.assertEqual(':%d' % xvfb.vdisplay_num, os.environ['DISPLAY'])
        self.assertIsNot(None, xvfb.proc)

    def test_start_with_args(self):
        w = 800
        h = 600
        depth = 16
        xvfb = Xvfb(width=w, height=h, colordepth=depth)
        self.addCleanup(xvfb.stop)
        xvfb.start()
        self.assertEqual(w, xvfb.width)
        self.assertEqual(h, xvfb.height)
        self.assertEqual(depth, xvfb.colordepth)
        self.assertEqual(os.environ['DISPLAY'], ':%d' % xvfb.vdisplay_num)
        self.assertIsNot(None, xvfb.proc)

    def test_stop(self):
        orig = os.environ['DISPLAY']
        xvfb = Xvfb()
        xvfb.start()
        self.assertNotEqual(orig, os.environ['DISPLAY'])
        xvfb.stop()
        self.assertEqual(orig, os.environ['DISPLAY'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
