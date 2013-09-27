#!/usr/bin/env python
#
#   * Corey Goldberg, 2012, 2013
#
#   * inspired by:
#       PyVirtualDisplay: http://pypi.python.org/pypi/PyVirtualDisplay


"""wrapper for running display inside X virtual framebuffer (Xvfb)"""


import os
import fnmatch
import random
import subprocess
import time


class Xvfb:

    def __init__(self, width=800, height=680, colordepth=24, **kwargs):
        self.width = width
        self.height = height
        self.colordepth = colordepth

        self.xvfb_cmd = [
            '-screen', '0', '%dx%dx%d' %
            (self.width, self.height, self.colordepth)
        ]

        for key, value in kwargs.items():
            self.xvfb_cmd = self.xvfb_cmd + ['-%s' % key, value]

        self.proc = None
        if 'DISPLAY' in os.environ:
            self.old_display_num = os.environ['DISPLAY'].split(':')[1]
        else:
            self.old_display_num = 0

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        self.vdisplay_num = self.search_for_free_display()
        self.xvfb_cmd = ['Xvfb', ':%d' % self.vdisplay_num] + self.xvfb_cmd

        self.proc = subprocess.Popen(self.xvfb_cmd,
                                     stdout=open(os.devnull),
                                     stderr=open(os.devnull),
                                     )
        time.sleep(0.2)  # give Xvfb time to start
        ret_code = self.proc.poll()
        if ret_code is None:
            self._redirect_display(self.vdisplay_num)
        else:
            self._redirect_display(self.old_display_num)
            self.proc = None
            print('Error: Xvfb did not start')

    def stop(self):
        self._redirect_display(self.old_display_num)
        if self.proc is not None:
            self.proc.kill()
            self.proc.wait()
            self.proc = None

    def search_for_free_display(self):
        ls = [int(x.split('X')[1].split('-')[0]) for x in self._lock_files()]
        min_display_num = 1000
        if len(ls):
            display_num = max(min_display_num, max(ls) + 1)
        else:
            display_num = min_display_num
        random.seed()
        display_num += random.randint(0, 100)
        return display_num

    def _lock_files(self):
        tmpdir = '/tmp'
        pattern = '.X*-lock'
        names = fnmatch.filter(os.listdir(tmpdir), pattern)
        ls = [os.path.join(tmpdir, child) for child in names]
        ls = [p for p in ls if os.path.isfile(p)]
        return ls

    def _redirect_display(self, display_num):
        os.environ['DISPLAY'] = ':%s' % display_num
