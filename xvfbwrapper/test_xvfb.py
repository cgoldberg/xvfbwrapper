#!/usr/bin/env python


from .xvfbwrapper import Xvfb

import os
import sys
import unittest

try:
    from StringIO import StringIO  # Python 2.7 compat
except ImportError:
    from io import StringIO

import pep8


class TestXvfb(unittest.TestCase):

    def test_start(self):
        xvfb = Xvfb()
        self.addCleanup(xvfb.stop)
        xvfb.start()
        self.assertEqual(':%d' % xvfb.vdisplay_num, os.environ['DISPLAY'])
        self.assertIsNot(None, xvfb.proc)

    def test_stop(self):
        orig_display = os.environ['DISPLAY']
        xvfb = Xvfb()
        xvfb.start()
        self.assertNotEqual(orig_display, os.environ['DISPLAY'])
        xvfb.stop()
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
        self.assertIsNot(None, xvfb.proc)

    def test_start_with_bad_kwarg_param(self):
        orig_display = os.environ['DISPLAY']
        out = StringIO()
        sys.stdout = out
        xvfb = Xvfb(nolisten='badvalue')
        self.addCleanup(xvfb.stop)
        xvfb.start()
        self.assertEqual(orig_display, os.environ['DISPLAY'])
        self.assertIsNone(xvfb.proc)
        self.assertIn('Error: Xvfb did not start', out.getvalue())

    def test_start_with_bad_kwarg(self):
        orig_display = os.environ['DISPLAY']
        out = StringIO()
        sys.stdout = out
        xvfb = Xvfb(badarg='foo')
        self.addCleanup(xvfb.stop)
        xvfb.start()
        self.assertEqual(orig_display, os.environ['DISPLAY'])
        self.assertIsNone(xvfb.proc)
        self.assertIn('Error: Xvfb did not start', out.getvalue())


class Pep8ConformanceTestCase(unittest.TestCase):
    """Test that all code conforms to PEP8."""
    def test_pep8_conformance(self):
        # scan source files in this directory recursively
        this_dir = os.path.dirname(os.path.realpath(__file__))
        self.pep8style = pep8.StyleGuide()
        self.pep8style.input_dir(this_dir)
        self.assertEqual(self.pep8style.options.report.total_errors, 0)
