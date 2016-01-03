#!/usr/bin/env python
#
#   * Corey Goldberg, 2012, 2013, 2015, 2016
#
#   * inspired by: PyVirtualDisplay


"""wrapper for running display inside X virtual framebuffer (Xvfb)"""


import os
import fnmatch
import random
import subprocess
import tempfile
import time


class Xvfb:

    def __init__(self, width=800, height=680, colordepth=24, **kwargs):
        self.width = width
        self.height = height
        self.colordepth = colordepth

        if not self._xvfb_exists():
            msg = 'Can not find Xvfb. Please install it and try again.'
            raise EnvironmentError(msg)

        self.xvfb_args = [
            '-screen', '0', '%dx%dx%d' %
            (self.width, self.height, self.colordepth)
        ]

        for key, value in kwargs.items():
            self.xvfb_args += ['-%s' % key, value]

        if 'DISPLAY' in os.environ:
            self.old_display_num = os.environ['DISPLAY'].split(':')[1]
        else:
            self.old_display_num = 0

        self.proc = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        self.vdisplay_num = self._get_next_unused_display()
        self.xvfb_cmd = ['Xvfb', ':%d' % self.vdisplay_num] + self.xvfb_args

        with open(os.devnull, 'w') as fnull:
            self.proc = subprocess.Popen(self.xvfb_cmd,
                                         stdout=fnull,
                                         stderr=fnull,
                                         close_fds=True)
        time.sleep(0.2)  # give Xvfb time to start
        ret_code = self.proc.poll()
        if ret_code is None:
            self._redirect_display(self.vdisplay_num)
        else:
            self._redirect_display(self.old_display_num)
            self.proc = None
            raise RuntimeError('Xvfb did not start')

    def stop(self):
        self._redirect_display(self.old_display_num)
        # TODO:
        # fix leaking X displays.
        # (killing Xvfb process doesn't clean up the underlying X11 server)
        if self.proc is not None:
            self.proc.kill()
            self.proc.wait()
            self.proc = None

    def _get_next_unused_display(self):
        tmpdir = tempfile.gettempdir()
        pattern = '.X*-lock'
        lockfile_names = fnmatch.filter(os.listdir(tmpdir), pattern)
        existing_displays = [int(name.split('X')[1].split('-')[0])
                             for name in lockfile_names]
        highest_display = max(existing_displays) if existing_displays else 0
        return highest_display + 1

    def _redirect_display(self, display_num):
        os.environ['DISPLAY'] = ':%s' % display_num

    def _xvfb_exists(self):
        """Check that Xvfb is in PATH and is executable."""
        return any(
            os.access(os.path.join(path, 'Xvfb'), os.X_OK)
            for path in os.environ['PATH'].split(os.pathsep)
        )
