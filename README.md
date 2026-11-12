# xvfbwrapper

### Manage headless displays with Xvfb (X virtual framebuffer)

----

## About

`xvfbwrapper` is a Python library for managing [X11][xorg-home] virtual displays
with [Xvfb (X virtual framebuffer)][xvfb-home], a virtual X server that runs
without a physical display. It provides the `Xvfb` class, a Python interface for
configuring and controlling the Xvfb program.

See the [module API documentation][api-docs] for more information.

- Copyright (c) 2012-2026 [Corey Goldberg][github-profile]
- Development: [GitHub][github-repo]
- Releases: [PyPI][pypi-home]
- License: [MIT][mit-license]

----

## Status

<table>
  <tr>
    <td>Latest Version</td>
    <td>
      <a href="https://pypi.org/project/xvfbwrapper">
        <img src="https://img.shields.io/pypi/v/xvfbwrapper.svg">
      </a>
    </td>
  </tr>
  <tr>
    <td>Tests (CI)</td>
    <td>
      <a href="https://github.com/cgoldberg/xvfbwrapper/actions/workflows/test.yml">
        <img src="https://github.com/cgoldberg/xvfbwrapper/actions/workflows/test.yml/badge.svg">
      </a>
    </td>
  </tr>
  <tr>
    <td>API Docs (CI)</td>
    <td>
      <a href="https://github.com/cgoldberg/xvfbwrapper/actions/workflows/docs.yml">
        <img src="https://github.com/cgoldberg/xvfbwrapper/actions/workflows/docs.yml/badge.svg">
      </a>
    </td>
  </tr>
  <tr>
    <td>Supported Python Versions</td>
    <td>
      <a href="https://pypi.org/project/xvfbwrapper">
        <img src="https://img.shields.io/pypi/pyversions/xvfbwrapper">
      </a>
    </td>
  </tr>
</table>

----

## What is Xvfb?

`Xvfb` (X virtual framebuffer) is a display server implementing the X11 display
server protocol. It runs in memory and does not require a physical display or
input device. Only a network layer is necessary.

`Xvfb` allows GUI applications that use X Windows to run on a headless system.

----

## Installation

Official releases are published on [PyPI][pypi-home]:

```
pip install xvfbwrapper
```

----

## System Requirements

- Python 3.11+
- X Window System
- Xvfb (`sudo apt install xvfb`, `sudo dnf install xorg-x11-server-Xvfb`, etc)
- Support for file locking using `fcntl` (POSIX systems)

----

## Usage

Always ensure that the virtual display is stopped, even if an exception occurs.
`Xvfb` can be used as a context manager or managed explicitly with
`try`/`finally`.

### Context Manager

```python
from xvfbwrapper import Xvfb

with Xvfb():
    # Runs inside the virtual display
    main()
```

The virtual display is automatically stopped when the context exits, including
if an exception occurs.

### Explicit Lifecycle Management

```python
from xvfbwrapper import Xvfb

xvfb = Xvfb()
xvfb.start()
try:
    # Runs inside the virtual display
    main()
finally:
    xvfb.stop()
```

### Specifying Display Geometry

```python
from xvfbwrapper import Xvfb

xvfb = Xvfb(width=1280, height=720)
xvfb.start()
```

### Setting `XDG_SESSION_TYPE`

When running `Xvfb` in a Wayland session, GUI toolkits may try to use the
Wayland backend instead of connecting to `Xvfb`. Setting
`set_xdg_session_type=True` forces `XDG_SESSION_TYPE=x11` in the Python process
and all child processes, ensuring that GUI apps use the X11 backend and can
render on the virtual display.

```python
from xvfbwrapper import Xvfb

xvfb = Xvfb(set_xdg_session_type=True)
xvfb.start()
```

### Specifying Other Xvfb Options

The `Xvfb` executable accepts several types of command line arguments.

The most common is an argument with a `-` prefix and a parameter (i.e.
`-nolisten tcp`). These can be added as keyword arguments when creating an
`xvfbwrapper.Xvfb` instance. For example:

```python
from xvfbwrapper import Xvfb

xvfb = Xvfb(nolisten="tcp")
# Xvfb will be called with the `-nolisten tcp` argument
xvfb.start()
```

There are other possible types of arguments:

- unary argument (i.e. `ttyxx`)
- unary argument with a `+` prefix (i.e. `+xinerama`)
- unary argument with a `-` prefix (i.e. `-nocursor`)
- argument with a parameter (i.e. `c 100`)
- argument with a `+` prefix and a parameter (i.e. `+extension RANDR`)

Any type of argument can be added as an `extra_args` sequence when creating an
`xvfbwrapper.Xvfb` instance. For example:

```python
from xvfbwrapper import Xvfb

xvfb = Xvfb(extra_args=("ttyxx", "-nocursor", "+extension", "RANDR"))
# Xvfb will be called with the `ttyxx -nocursor +extension RANDR` arguments
xvfb.start()
```

### Running Multiple Displays

When running multiple Xvfb instances concurrently, each instance should have its
own environment dictionary to avoid conflicts. Pass a separate copy of
`os.environ` to each instance using the `environ` argument.

Use `os.environ.copy()` rather than passing `os.environ` directly. This ensures
each instance has its own environment dictionary.

```python
import os

from xvfbwrapper import Xvfb

xvfb1 = Xvfb(environ=os.environ.copy())
xvfb2 = Xvfb(environ=os.environ.copy())

xvfb1.start()
xvfb2.start()

try:
    # Use each Xvfb instance independently
    ...
finally:
    xvfb1.stop()
    xvfb2.stop()
```

## Examples

### Headless Browser Testing With `unittest`

The following example uses [`selenium`][selenium-home] and `xvfbwrapper` to run
Chrome tests inside a virtual display.

```python
import unittest

from selenium import webdriver
from xvfbwrapper import Xvfb


class TestPage(unittest.TestCase):
    def setUp(self):
        xvfb = Xvfb(set_xdg_session_type=True)
        xvfb.start()
        self.addCleanup(xvfb.stop)
        self.driver = webdriver.Chrome()
        self.addCleanup(self.driver.quit)

    def test_selenium_homepage(self):
        self.driver.get("https://selenium.dev")
        self.assertIn("Selenium", self.driver.title)
```

### Headless Browser Testing With `pytest`

The same setup can be used with `pytest` by managing the virtual display and
browser through a fixture.

```python
import pytest

from selenium import webdriver
from xvfbwrapper import Xvfb


@pytest.fixture
def driver():
    with Xvfb(set_xdg_session_type=True):
        driver = webdriver.Chrome()
        yield driver
        driver.quit()


def test_selenium_homepage(driver):
    driver.get("https://selenium.dev")
    assert "Selenium" in driver.title
```

[api-docs]: https://coreygoldberg.com/xvfbwrapper
[github-profile]: https://github.com/cgoldberg
[github-repo]: https://github.com/cgoldberg/xvfbwrapper
[mit-license]: https://raw.githubusercontent.com/cgoldberg/xvfbwrapper/refs/heads/master/LICENSE
[pypi-home]: https://pypi.org/project/xvfbwrapper
[selenium-home]: https://selenium.dev
[xorg-home]: https://www.x.org
[xvfb-home]: https://x.org/releases/X11R7.7/doc/man/man1/Xvfb.1.xhtml
