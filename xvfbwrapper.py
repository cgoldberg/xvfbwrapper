# Corey Goldberg, 2012-2026
# License: MIT

"""Run a headless display inside X virtual framebuffer (Xvfb)."""

import os
import platform
import shutil
import subprocess
import tempfile
import time
from collections.abc import MutableMapping, Sequence
from contextlib import suppress
from pathlib import Path

try:
    import fcntl
except ImportError:
    system = platform.system()
    raise OSError(f"xvfbwrapper is not supported on this platform: {system}")

from random import randint


class Xvfb:
    # Maximum value to use for a display. 32-bit maxint is the
    # highest Xvfb currently supports
    MAX_DISPLAY = 2147483647

    def __init__(
        self,
        width: int = 800,
        height: int = 680,
        colordepth: int = 24,
        tempdir: Path | str | None = None,
        display: int | None = None,
        environ: MutableMapping[str, str] | None = None,
        extra_args: Sequence[str] | None = None,
        timeout: int = 10,
        **kwargs,
    ):
        self.width: int = width
        self.height: int = height
        self.colordepth: int = colordepth
        self._tempdir: Path | str = tempdir or tempfile.gettempdir()
        self._timeout: int = timeout
        self.new_display: int | None = display
        self.environ: MutableMapping[str, str] = environ or os.environ

        if not self._xvfb_exists():
            raise OSError("Could not find Xvfb. Please install it and try again")

        self.xvfb_cmd: list[str] = []

        if not extra_args:
            extra_args = []

        self.extra_xvfb_args = [
            "-screen",
            "0",
            f"{self.width}x{self.height}x{self.colordepth}",
            *extra_args,
        ]

        for key, value in kwargs.items():
            self.extra_xvfb_args += [f"-{key}", value]

        self.orig_display_var: str | None
        if "DISPLAY" in self.environ:
            self.orig_display_var = self.environ["DISPLAY"]
        else:
            self.orig_display_var = None

        self.proc: subprocess.Popen[bytes] | None = None

    def __enter__(self) -> "Xvfb":
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self) -> None:
        if not os.access(self._tempdir, os.W_OK):
            raise RuntimeError(
                f"Could not access writable temp directory: {self._tempdir}"
            )
        if self.new_display is not None:
            if not self._get_lock_for_display(self.new_display):
                raise RuntimeError(f"Could not lock display :{self.new_display}")
        else:
            self.new_display = self._get_next_unused_display()
        display_var = f":{self.new_display}"
        self.xvfb_cmd = ["Xvfb", display_var, *self.extra_xvfb_args]
        self.proc = subprocess.Popen(
            self.xvfb_cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
        )
        start = time.time()
        while not self._local_display_exists(self.new_display):
            time.sleep(1e-3)
            if time.time() - start > self._timeout:
                self.stop()
                raise RuntimeError(f"Xvfb display did not open: {self.xvfb_cmd}")
        ret_code = self.proc.poll()
        if ret_code is None:
            self._set_display(display_var)
        else:
            self._cleanup_lock_file()
            raise RuntimeError(f"Xvfb did not start ({ret_code}): {self.xvfb_cmd}")

    def stop(self) -> None:
        if self.proc is None:
            return
        try:
            if self.orig_display_var is None:
                self.environ.pop("DISPLAY", None)
            else:
                self._set_display(self.orig_display_var)
            if self.proc is not None:
                with suppress(OSError):
                    self.proc.terminate()
                    self.proc.wait(self._timeout)
                self.proc = None
        finally:
            self._cleanup_lock_file()

    def _xvfb_exists(self) -> bool:
        """Check that Xvfb is available on PATH and is executable."""
        return True if shutil.which("Xvfb") is not None else False

    def _cleanup_lock_file(self):
        """Delete lock files when stopping.

        This gets called if the process exits safely with Xvfb.stop(),
        whether called explicitly, or by __exit__.

        If you are ending up with /tmp/X123-lock files when Xvfb is not
        running, then Xvfb is not exiting cleanly. Always either call
        Xvfb.stop() in a finally block, or use Xvfb as a context manager
        to ensure lock files are purged.
        """
        self._lock_display_file.close()
        with suppress(OSError):
            Path(self._lock_display_file.name).unlink()

    def _get_lock_for_display(self, display) -> bool:
        """Attempt to acquire an exclusive lock for a display.

        In order to ensure multi-process safety, this method attempts
        to acquire an exclusive lock on a temporary file whose name
        contains the display number for Xvfb.
        """
        tempfile_path = Path(self._tempdir, f".X{display}-lock")
        try:
            self._lock_display_file = tempfile_path.open("w")
        except PermissionError:
            return False
        else:
            try:
                fcntl.flock(self._lock_display_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                return False
            else:
                return True

    def _get_next_unused_display(self) -> int:
        """Randomly choose a display number and try to acquire a lock for it.

        If the lock could be acquired, return the display number, otherwise
        choose a new one.
        """
        while True:
            rand = randint(1, self.__class__.MAX_DISPLAY)
            if self._get_lock_for_display(rand):
                return rand

    def _local_display_exists(self, display) -> bool:
        tempdir = "/tmp"
        # We need read access to the real system temp directory
        if not os.access(tempdir, os.R_OK):
            raise RuntimeError(f"Could not access {tempdir} directory: {self._tempdir}")
        return Path(tempdir, ".X11-unix", f"X{display}").exists()

    def _set_display(self, display_var):
        self.environ["DISPLAY"] = display_var
