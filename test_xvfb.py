#!/usr/bin/env python

import os
import unittest

from xvfbwrapper import Xvfb


class TestXvfb(unittest.TestCase):

    def reset_display(self):
        os.environ['DISPLAY'] = ':0'

    def setUp(self):
        self.reset_display()

    def test_start(self):
        xvfb = Xvfb()
        self.addCleanup(xvfb.stop)
        xvfb.start()
        display_var = ':{}'.format(xvfb.new_display)
        self.assertEqual(display_var, os.environ['DISPLAY'])
        self.assertIsNotNone(xvfb.proc)

    def test_stop(self):
        orig_display = os.environ['DISPLAY']
        xvfb = Xvfb()
        xvfb.start()
        self.assertNotEqual(orig_display, os.environ['DISPLAY'])
        xvfb.stop()
        self.assertEqual(orig_display, os.environ['DISPLAY'])
        self.assertIsNone(xvfb.proc)

    def test_start_without_existing_display(self):
        del os.environ['DISPLAY']
        xvfb = Xvfb()
        self.addCleanup(xvfb.stop)
        self.addCleanup(self.reset_display)
        xvfb.start()
        display_var = ':{}'.format(xvfb.new_display)
        self.assertEqual(display_var, os.environ['DISPLAY'])
        self.assertIsNotNone(xvfb.proc)

    def test_as_context_manager(self):
        orig_display = os.environ['DISPLAY']
        with Xvfb() as xvfb:
            display_var = ':{}'.format(xvfb.new_display)
            self.assertEqual(display_var, os.environ['DISPLAY'])
            self.assertIsNotNone(xvfb.proc)
        self.assertEqual(orig_display, os.environ['DISPLAY'])
        self.assertIsNone(xvfb.proc)

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
        display_var = ':{}'.format(xvfb.new_display)
        self.assertEqual(display_var, os.environ['DISPLAY'])
        self.assertIsNotNone(xvfb.proc)

    def test_start_with_arbitrary_kwargs(self):
        xvfb = Xvfb(nolisten='tcp')
        self.addCleanup(xvfb.stop)
        xvfb.start()
        display_var = ':{}'.format(xvfb.new_display)
        self.assertEqual(display_var, os.environ['DISPLAY'])
        self.assertIsNotNone(xvfb.proc)

    def test_start_fails_with_unknown_kwargs(self):
        xvfb = Xvfb(foo='bar')
        with self.assertRaises(RuntimeError):
            xvfb.start()
