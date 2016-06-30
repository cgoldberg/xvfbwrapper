#!/usr/bin/env python
#
#   * Corey Goldberg, 2012, 2013, 2015, 2016
#
#   * inspired by: PyVirtualDisplay


"""wrapper for running display inside X virtual framebuffer (Xvfb)"""


import os
import subprocess
import tempfile
import time
import fcntl
from random import randint

try:
    BlockingIOError
except NameError:
    # python 2
    BlockingIOError = IOError


class Xvfb(object):

    # Maximum value to use for a display. 32-bit maxint is the
    # highest Xvfb currently supports
    MAX_DISPLAY = 2147483647
    SLEEP_TIME_BEFORE_START = 0.1

    def __init__(self, width=800, height=680, colordepth=24, tempdir=None,
                 **kwargs):
        self.width = width
        self.height = height
        self.colordepth = colordepth
        self._tempdir = tempdir or tempfile.gettempdir()

        if not self.xvfb_exists():
            msg = 'Can not find Xvfb. Please install it and try again.'
            raise EnvironmentError(msg)

        self.extra_xvfb_args = ['-screen', '0', '{}x{}x{}'.format(
                                self.width, self.height, self.colordepth)]

        for key, value in kwargs.items():
            self.extra_xvfb_args += ['-{}'.format(key), value]

        if 'DISPLAY' in os.environ:
            self.orig_display = os.environ['DISPLAY'].split(':')[1]
        else:
            self.orig_display = None

        self.proc = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        self.new_display = self._get_next_unused_display()
        display_var = ':{}'.format(self.new_display)
        self.xvfb_cmd = ['Xvfb', display_var] + self.extra_xvfb_args
        with open(os.devnull, 'w') as fnull:
            self.proc = subprocess.Popen(self.xvfb_cmd,
                                         stdout=fnull,
                                         stderr=fnull,
                                         close_fds=True)
        # give Xvfb time to start
        time.sleep(self.__class__.SLEEP_TIME_BEFORE_START)
        ret_code = self.proc.poll()
        if ret_code is None:
            self._set_display_var(self.new_display)
        else:
            self._cleanup_lock_file()
            raise RuntimeError('Xvfb did not start')

    def stop(self):
        try:
            if self.orig_display is None:
                del os.environ['DISPLAY']
            else:
                self._set_display_var(self.orig_display)
            if self.proc is not None:
                try:
                    self.proc.terminate()
                    self.proc.wait()
                except OSError:
                    pass
                self.proc = None
        finally:
            self._cleanup_lock_file()

    def _cleanup_lock_file(self):
        '''
        This should always get called if the process exits safely
        with Xvfb.stop() (whether called explicitly, or by __exit__).

        If you are ending up with /tmp/X123-lock files when Xvfb is not
        running, then Xvfb is not exiting cleanly. Always either call
        Xvfb.stop() in a finally block, or use Xvfb as a context manager
        to ensure lock files are purged.

        '''
        self._lock_display_file.close()
        try:
            os.remove(self._lock_display_file.name)
        except OSError:
            pass

    def _get_next_unused_display(self):
        '''
        In order to ensure multi-process safety, this method attempts
        to acquire an exclusive lock on a temporary file whose name
        contains the display number for Xvfb.
        '''
        tempfile_path = os.path.join(self._tempdir, '.X{0}-lock')
        while True:
            rand = randint(1, self.__class__.MAX_DISPLAY)
            self._lock_display_file = open(tempfile_path.format(rand), 'w')
            try:
                fcntl.flock(self._lock_display_file,
                            fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                continue
            else:
                return rand

    def _set_display_var(self, display):
        os.environ['DISPLAY'] = ':{}'.format(display)

    def xvfb_exists(self):
        """Check that Xvfb is available on PATH and is executable."""
        paths = os.environ['PATH'].split(os.pathsep)
        return any(os.access(os.path.join(path, 'Xvfb'), os.X_OK)
                   for path in paths)
