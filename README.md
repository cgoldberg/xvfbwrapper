# xvfbwrapper

### Manage headless displays with Xvfb (X virtual framebuffer)

----

[![Supported Python Versions](https://img.shields.io/pypi/pyversions/xvfbwrapper)](https://pypi.org/project/xvfbwrapper)

- Copyright (c) 2012-2026 [Corey Goldberg][github-profile]
- Development: [GitHub][github-repo]
- Releases: [PyPI][pypi-home]
- License: [MIT][mit-license]

----

## About

`xvfbwrapper` is a Python library for controlling X11 virtual displays with Xvfb.

----

## What is Xvfb?


`Xvfb` (X virtual framebuffer) is a display server implementing the X11
display server protocol. It runs in memory and does not require a physical
display or input device. Only a network layer is necessary.

`Xvfb` allows GUI applications that use X Windows to run on a headless system.

----

## Installation

Official releases are published on [PyPI][pypi-home]:

```
pip install xvfbwrapper
```

----

## System Requirements

- Python 3.10+
- X Window System (or Xwayland)
- Xvfb (`sudo apt-get install xvfb`, `yum install xorg-x11-server-Xvfb`, etc)
- Support for locking with `fcntl` system call (non-Windows systems)

----

## Examples

#### Basic Usage:

Note: Always either wrap your usage of `Xvfb()` with try/finally, or use it as
a context manager to ensure the display is stopped. If you don't, you'll end up
with a bunch of junk in `/tmp` if errors occur.

```python
from xvfbwrapper import Xvfb

xvfb = Xvfb()
xvfb.start()
try:
    # launch stuff inside virtual display here
finally:
    xvfb.stop()
```

#### Usage as a context manager:

```python
from xvfbwrapper import Xvfb

with Xvfb():
    # launch stuff inside virtual display here
    # (Xvfb will stop when this block completes)
```

#### Specifying display geometry:

```python
from xvfbwrapper import Xvfb

xvfb = Xvfb(width=1280, height=720)
xvfb.start()
```

#### Specifying display number:

```python
from xvfbwrapper import Xvfb

xvfb = Xvfb(display=23)
xvfb.start() # Xvfb will start on display :23
```

#### Specifying other Xvfb options:

The `Xvfb` executable accepts several types of command line arguments.

The most common is an argument with a `-` prefix and a parameter
(i.e. `-nolisten tcp`). These can be added as keyword arguments when
creating an `xvfbrwapper.Xvfb` instance. For example:

```python
from xvfbwrapper import Xvfb

xvfb = Xvfb(nolisten="tcp")
xvfb.start() # Xvfb will be called with the `-nolisten tcp` argument
```

However, there are other possible types of arguments:

- unary argument (i.e. `ttyxx`)
- unary argument with a `+` prefix (i.e. `+xinerama`)
- unary argument with a `-` prefix (i.e. `-nocursor`)
- argument with a parameter (i.e. `c 100`)
- argument with a `+` prefix and a parameter (i.e. `+extension RANDR`)

Any type of argument can be added as an `extra_args` sequence when creating
an `xvfbrwapper.Xvfb` instance. For example:

```python
from xvfbwrapper import Xvfb

xvfb = Xvfb(extra_args=("ttyxx", "-nocursor", "+extension", "RANDR"))
xvfb.start() # Xvfb will be called with the `ttyxx -nocursor +extension RANDR` arguments
```

#### Multithreaded execution:

To run several Xvfb displays at the same time, you can use the `environ`
keyword when starting the `Xvfb` instances. This provides isolation between
processes or threads. Be sure to use the environment dictionary you initialize
`Xvfb` with in your subsequent calls. Also, if you wish to inherit your current
environment, you must use the copy method of `os.environ` and not simply
assign a new variable to `os.environ`:

```python
import os

from xvfbwrapper import Xvfb

isolated_environment1 = os.environ.copy()
xvfb1 = Xvfb(environ=isolated_environment1)
xvfb1.start()

isolated_environment2 = os.environ.copy()
xvfb2 = Xvfb(environ=isolated_environment2)
xvfb2.start()

try:
    # launch stuff inside virtual displays here
finally:
    xvfb1.stop()
    xvfb2.stop()
```

#### Usage in testing - headless Selenium WebDriver tests:

This is a test using `selenium` and `xvfbwrapper` to run tests
on Chrome with a headless display. (see: [selenium docs][selenium-docs])

[selenium-docs]: https://www.selenium.dev/selenium/docs/api/py

```python
import os
import unittest

from selenium import webdriver
from xvfbwrapper import Xvfb

# force X11 in case we are running on a Wayland system
os.environ["XDG_SESSION_TYPE"] = "x11"


class TestPage(unittest.TestCase):

    def setUp(self):
        xvfb = Xvfb()
        xvfb.start()
        self.driver = webdriver.Chrome()
        self.addCleanup(xvfb.stop)
        self.addCleanup(self.driver.quit)

    def test_selenium_homepage(self):
        self.driver.get("https://www.selenium.dev")
        self.assertIn("Selenium", self.driver.title)


if __name__ == "__main__":
    unittest.main()
```

- virtual display is launched
- browser launches inside virtual display (headless)
- browser quits during cleanup
- virtual display stops during cleanup

----

## xvfbwrapper Issues

To report a bug or request a new feature, please open an issue on [GitHub][github-issues].

----

## xvfbwrapper Development

1. Fork the project repo on [GitHub][github-repo]

2. Clone the repo:

    ```
    git clone https://github.com/<USERNAME>/xvfbwrapper.git
    cd xvfbwrapper
    ```

3. Make changes and run the tests:

    Create a virtual env and install required testing packages:

    ```
    python -m venv venv
    source ./venv/bin/activate
    pip install --editable --group dev --group test .
    ```

    Run all tests in the default Python environment:

    ```
    pytest
    ```

    Run all tests, linting, and type checking across all supported/installed
    Python environments:

    ```
    tox
    ```

4. Commit and push your changes

5. Submit a [Pull Request][github-prs]


[github-profile]: https://github.com/cgoldberg
[github-repo]: https://github.com/cgoldberg/xvfbwrapper
[github-issues]: https://github.com/cgoldberg/xvfbwrapper/issues
[github-prs]: https://github.com/cgoldberg/xvfbwrapper/pulls
[pypi-home]: https://pypi.org/project/xvfbwrapper
[mit-license]: https://raw.githubusercontent.com/cgoldberg/xvfbwrapper/refs/heads/master/LICENSE
