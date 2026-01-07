#!/usr/bin/env python3


"""Tests for xvfbwrapper."""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch

from xvfbwrapper import Xvfb


def contains_sublist(lst, sub_lst):
    if not sub_lst:
        return True
    n, m = len(lst), len(sub_lst)
    return any(lst[i : i + m] == sub_lst for i in range(n - m + 1))


# Using mock.patch as a class decorator applies it to every
# test_* method and removes it after test completes.
#
# Force X11 in case we are running on a Wayland system
@patch.dict("os.environ", {"XDG_SESSION_TYPE": "x11"})
@patch.dict("os.environ", {"DISPLAY": ":0"})
class TestXvfb(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_xvfb_binary_does_not_exist(self):
        with patch("xvfbwrapper.Xvfb._xvfb_exists") as xvfb_exists:
            xvfb_exists.return_value = False
            with self.assertRaisesRegex(
                EnvironmentError, "Could not find Xvfb. Please install it and try again"
            ):
                Xvfb()

    def test_default_args(self):
        w = 800
        h = 680
        depth = 24
        xvfb = Xvfb()
        self.assertEqual(w, xvfb.width)
        self.assertEqual(h, xvfb.height)
        self.assertEqual(depth, xvfb.colordepth)
        self.assertEqual(["-screen", "0", f"{w}x{h}x{depth}"], xvfb.extra_xvfb_args)

    def test_kwargs(self):
        w = 610
        h = 620
        depth = 8
        xvfb = Xvfb(width=w, height=h, colordepth=depth)
        self.assertEqual(w, xvfb.width)
        self.assertEqual(h, xvfb.height)
        self.assertEqual(depth, xvfb.colordepth)
        self.assertEqual(["-screen", "0", f"{w}x{h}x{depth}"], xvfb.extra_xvfb_args)

    def test_extra_kwargs(self):
        extra_args = ["-nocursor", "+extension", "RANDR"]
        xvfb = Xvfb(extra_args=extra_args)
        self.assertEqual(
            ["-screen", "0", f"{800}x{680}x{24}", *extra_args], xvfb.extra_xvfb_args
        )

    def test_start(self):
        xvfb = Xvfb()
        self.addCleanup(xvfb.stop)
        xvfb.start()
        self.assertEqual(f":{xvfb.new_display}", os.environ["DISPLAY"])
        self.assertIsNotNone(xvfb.proc)

    def test_stop(self):
        orig_display = os.environ["DISPLAY"]
        xvfb = Xvfb()
        xvfb.start()
        self.assertNotEqual(orig_display, os.environ["DISPLAY"])
        xvfb.stop()
        self.assertEqual(orig_display, os.environ["DISPLAY"])
        self.assertIsNone(xvfb.proc)

    def test_start_multiple_times(self):
        xvfb = Xvfb()
        xvfb.start()
        self.addCleanup(xvfb.stop)
        pid1 = xvfb.proc.pid
        xvfb.stop()
        xvfb.start()
        pid2 = xvfb.proc.pid
        self.assertIsNotNone(xvfb.proc)
        self.assertNotEqual(pid1, pid2)

    def test_stop_if_not_running_doesnt_raise_error(self):
        xvfb = Xvfb()
        xvfb.stop()
        self.assertIsNone(xvfb.proc)

    def test_stop_with_xquartz(self):
        # Check that xquartz pattern for display server is dealt with by
        # xvfb.stop() and restored appropriately
        xquartz_display = (
            "/private/tmp/com.apple.launchd.CgDzCWvNb1/org.macosforge.xquartz:0"
        )
        with patch.dict("os.environ", {"DISPLAY": xquartz_display}):
            xvfb = Xvfb()
            xvfb.start()
            self.assertNotEqual(xquartz_display, os.environ["DISPLAY"])
            xvfb.stop()
            self.assertEqual(xquartz_display, os.environ["DISPLAY"])
        self.assertIsNone(xvfb.proc)

    def test_start_and_stop_as_context_manager(self):
        orig_display = os.environ["DISPLAY"]
        with Xvfb() as xvfb:
            self.assertEqual(f":{xvfb.new_display}", os.environ["DISPLAY"])
            self.assertIsNotNone(xvfb.proc)
        self.assertEqual(orig_display, os.environ["DISPLAY"])
        self.assertIsNone(xvfb.proc)

    def test_start_with_tempdir(self):
        with tempfile.TemporaryDirectory() as tempdir:
            xvfb = Xvfb(tempdir=tempdir)
            self.addCleanup(xvfb.stop)
            xvfb.start()
            self.assertIsNotNone(xvfb.proc)

    def test_start_with_unwritable_tempdir(self):
        unwriteable_dir = "/etc"
        xvfb = Xvfb(tempdir=unwriteable_dir)
        with self.assertRaisesRegex(
            RuntimeError, f"Could not access writable temp directory: {unwriteable_dir}"
        ):
            xvfb.start()
        self.assertIsNone(xvfb.proc)

    def test_start_with_unknown_tempdir(self):
        unknown_dir = "/tmp/some_unknown_path"
        xvfb = Xvfb(tempdir=unknown_dir)
        with self.assertRaisesRegex(
            RuntimeError, f"Could not access writable temp directory: {unknown_dir}"
        ):
            xvfb.start()
        self.assertIsNone(xvfb.proc)

    def test_start_without_existing_display(self):
        with patch.dict("os.environ", {}):
            del os.environ["DISPLAY"]
            xvfb = Xvfb()
            self.addCleanup(xvfb.stop)
            xvfb.start()
            self.assertEqual(f":{xvfb.new_display}", os.environ["DISPLAY"])
        self.assertIsNotNone(xvfb.proc)

    def test_start_with_empty_display(self):
        with patch.dict("os.environ", {}):
            os.environ["DISPLAY"] = ""
            xvfb = Xvfb()
            self.addCleanup(xvfb.stop)
            xvfb.start()
            self.assertEqual(f":{xvfb.new_display}", os.environ["DISPLAY"])
        self.assertIsNotNone(xvfb.proc)

    def test_start_with_specific_display(self):
        display_num = 42
        xvfb = Xvfb(display=display_num)
        self.addCleanup(xvfb.stop)
        xvfb.start()
        assert ":42" in xvfb.xvfb_cmd
        self.assertEqual(xvfb.new_display, display_num)
        self.assertIsNotNone(xvfb.proc)

    def test_start_on_used_display(self):
        display_num = 42
        xvfb = Xvfb(display=display_num)
        xvfb2 = Xvfb(display=display_num)
        self.addCleanup(xvfb.stop)
        xvfb.start()
        self.assertEqual(xvfb.new_display, display_num)
        self.assertIsNotNone(xvfb.proc)
        with self.assertRaisesRegex(
            RuntimeError, f"Could not lock display :{display_num}"
        ):
            xvfb2.start()

    def test_start_with_kwargs(self):
        w = 600
        h = 600
        depth = 16
        xvfb = Xvfb(width=w, height=h, colordepth=depth)
        self.addCleanup(xvfb.stop)
        xvfb.start()
        assert f"{w}x{h}x{depth}" in xvfb.xvfb_cmd
        self.assertEqual(f":{xvfb.new_display}", os.environ["DISPLAY"])
        self.assertIsNotNone(xvfb.proc)

    def test_start_with_arbitrary_kwargs(self):
        xvfb = Xvfb(nolisten="tcp")
        self.addCleanup(xvfb.stop)
        xvfb.start()
        assert contains_sublist(xvfb.xvfb_cmd, ["-nolisten", "tcp"])
        self.assertEqual(f":{xvfb.new_display}", os.environ["DISPLAY"])
        self.assertIsNotNone(xvfb.proc)

    def test_start_with_extra_args(self):
        extra_args = ["-nocursor", "+extension", "RANDR"]
        xvfb = Xvfb(extra_args=extra_args)
        self.addCleanup(xvfb.stop)
        xvfb.start()
        assert contains_sublist(xvfb.xvfb_cmd, extra_args)
        self.assertEqual(f":{xvfb.new_display}", os.environ["DISPLAY"])
        self.assertIsNotNone(xvfb.proc)

    def test_start_fails_with_unknown_kwargs(self):
        xvfb = Xvfb(foo="bar", timeout=5)
        expected_cmd_args = [
            "Xvfb",
            r":\d",
            "-screen",
            r"0",
            r"\dx\dx\d",
            "-foo",
            "bar",
        ]
        with self.assertRaisesRegex(
            RuntimeError, f"Xvfb display did not open: {expected_cmd_args}"
        ):
            xvfb.start()
        self.assertIsNone(xvfb.proc)

    def test_get_next_unused_display_does_not_reuse_lock(self):
        xvfb = Xvfb()
        xvfb2 = Xvfb()
        xvfb3 = Xvfb()
        self.addCleanup(xvfb._cleanup_lock_file)
        self.addCleanup(xvfb2._cleanup_lock_file)
        self.addCleanup(xvfb3._cleanup_lock_file)
        side_effect = [11, 11, 22, 11, 22, 11, 22, 22, 22, 33]
        with patch("xvfbwrapper.randint", side_effect=side_effect) as mockrandint:
            self.assertEqual(xvfb._get_next_unused_display(), 11)
            self.assertEqual(mockrandint.call_count, 1)
            if sys.implementation.name == "cpython":
                # ResourceWarning is only raised on CPython because
                # of an implementation detail in it's garbage collector.
                # This does not occur on other Python implementations
                # (like PyPy).
                with self.assertWarns(ResourceWarning):
                    self.assertEqual(xvfb2._get_next_unused_display(), 22)
                    self.assertEqual(mockrandint.call_count, 3)
                    self.assertEqual(xvfb3._get_next_unused_display(), 33)
                    self.assertEqual(mockrandint.call_count, 10)
            else:
                self.assertEqual(xvfb2._get_next_unused_display(), 22)
                self.assertEqual(mockrandint.call_count, 3)
                self.assertEqual(xvfb3._get_next_unused_display(), 33)
                self.assertEqual(mockrandint.call_count, 10)

    def test_environ_keyword_isolates_environment_modification(self):
        # Check that start and stop methods modified the environ dict if
        # passed and does not modify os.environ
        env_duped = os.environ.copy()
        xvfb = Xvfb(environ=env_duped)
        xvfb.start()
        new_display = f":{xvfb.new_display}"
        self.assertEqual(":0", os.environ["DISPLAY"])
        self.assertEqual(new_display, env_duped["DISPLAY"])
        xvfb.stop()
        self.assertEqual(":0", os.environ["DISPLAY"])
        self.assertEqual(":0", env_duped["DISPLAY"])
        self.assertIsNone(xvfb.proc)

    def test_start_failure_without_initial_display_env(self):
        # Provide a custom env *without* DISPLAY so orig_display_var == None
        custom_env = {"PATH": os.environ.get("PATH", "")}
        xvfb = Xvfb(timeout=0.5, environ=custom_env)
        # Ensure any spawned proc is cleaned up
        self.addCleanup(lambda: xvfb.proc and xvfb.proc.terminate())
        expected_cmd_args = [
            "Xvfb",
            r":\d",
            "-screen",
            r"0",
            r"\dx\dx\d",
            "-foo",
            "bar",
        ]
        # Force the display socket to never appear
        with patch.object(xvfb, "_local_display_exists", return_value=False):
            with self.assertRaisesRegex(
                RuntimeError, f"Xvfb display did not open: {expected_cmd_args}"
            ):
                xvfb.start()
        # After failure, calling stop() again must not raise an exception
        xvfb.stop()
        # We never injected DISPLAY into our custom env
        self.assertNotIn("DISPLAY", custom_env)
        self.assertIsNone(xvfb.proc)


if __name__ == "__main__":
    unittest.main(verbosity=2)
