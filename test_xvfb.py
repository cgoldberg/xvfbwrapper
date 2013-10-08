#!/usr/bin/env python


from xvfbwrapper import Xvfb

import os
import sys
import unittest


class TestXvfb(unittest.TestCase):

    def setUp(self):
        sys.stdout = sys.__stdout__
        self.addCleanup(self.restore_stdout)

    def restore_stdout(self):
        sys.stdout = sys.__stdout__

    def test_start(self):
        xvfb = Xvfb()
        self.addCleanup(xvfb.stop)
        xvfb.start()
        self.assertEqual(':%d' % xvfb.vdisplay_num, os.environ['DISPLAY'])
        self.assertIsNotNone(xvfb.proc)

    def test_stop(self):
        orig_display = os.environ['DISPLAY']
        xvfb = Xvfb()
        xvfb.start()
        self.assertNotEqual(orig_display, os.environ['DISPLAY'])
        xvfb.stop()
        self.assertIsNone(xvfb.proc)
        self.assertEqual(orig_display, os.environ['DISPLAY'])

    def test_as_context_manager(self):
        orig_display = os.environ['DISPLAY']
        with Xvfb() as xvfb:
            self.assertEqual(':%d' % xvfb.vdisplay_num, os.environ['DISPLAY'])
            self.assertIsNotNone(xvfb.proc)
        self.assertIsNone(xvfb.proc)
        self.assertEqual(orig_display, os.environ['DISPLAY'])

    def test_start_with_kwargs(self):
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
        self.assertIsNotNone(xvfb.proc)

    def test_start_with_arbitrary_kwarg(self):
        xvfb = Xvfb(nolisten='tcp')
        self.addCleanup(xvfb.stop)
        xvfb.start()
        self.assertEqual(os.environ['DISPLAY'], ':%d' % xvfb.vdisplay_num)
        self.assertIsNotNone(xvfb.proc)
