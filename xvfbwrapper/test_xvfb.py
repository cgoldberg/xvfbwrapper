#!/usr/bin/env python


from .xvfbwrapper import Xvfb

import os
import unittest

import pep8


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


class Pep8ConformanceTestCase(unittest.TestCase):
    """Test that all code conforms to PEP8."""
    def test_pep8_conformance(self):
        # scan source files in this directory recursively
        this_dir = os.path.dirname(os.path.realpath(__file__))
        self.pep8style = pep8.StyleGuide()
        self.pep8style.input_dir(this_dir)
        self.assertEqual(self.pep8style.options.report.total_errors, 0)
