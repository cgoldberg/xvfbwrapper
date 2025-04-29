# xvfbwrapper

#### Manage headless displays with Xvfb (X virtual framebuffer)

- Copyright (c) 2012-2025 [Corey Goldberg][github-home]
- Development: [GitHub][github-repo]
- Releases: [PyPI][pypi]
- License: [MIT][mit-license]

[github-home]: https://github.com/cgoldberg
[github-repo]: https://github.com/cgoldberg/xvfbwrapper
[pypi]: https://pypi.org/project/xvfbwrapper
[mit-license]: https://raw.githubusercontent.com/cgoldberg/xvfbwrapper/refs/heads/master/LICENSE

----

## About

`xvfbwrapper` is a python module for controlling X11 virtual displays with Xvfb.

----

## What is Xvfb?


`Xvfb` (X virtual framebuffer) is a display server implementing the X11
display server protocol. It runs in memory and does not require a physical
display or input devices. Only a network layer is necessary.

`Xvfb` is useful for programs that run on a headless servers, but require X Windows.

----

## Installation

```
pip install xvfbwrapper
```

----

## System Requirements

- Python 3.9+
- X Window System
- Xvfb (`sudo apt-get install xvfb`, `yum install xorg-x11-server-Xvfb`, etc)
- File locking with `fcntl`

----

## Examples

#### Basic Usage:

```python
from xvfbwrapper import Xvfb

xvfb = Xvfb()
xvfb.start()
try:
    # launch stuff inside virtual display here
finally:
    # always either wrap your usage of Xvfb() with try/finally, or
    # alternatively use Xvfb() as a context manager. If you don't,
    # you'll probably end up with a bunch of junk in /tmp
    xvfb.stop()
```

#### Specifying display geometry:

```python
from xvfbwrapper import Xvfb

xvfb = Xvfb(width=1280, height=740)
xvfb.start()
try:
    # launch stuff inside virtual display here
finally:
    xvfb.stop()
```

#### Specifying display number:

```python
from xvfbwrapper import Xvfb

xvfb = Xvfb(display=23)
xvfb.start()
# Xvfb is started with display :23
# see vdisplay.new_display
try:
    # launch stuff inside virtual display here
finally:
    xvfb.stop()
```

#### Usage as a context manager:

```python
from xvfbwrapper import Xvfb

with Xvfb() as xvfb:
    # launch stuff inside virtual display here
    # Xvfb will stop when this block completes
```

#### Multithreaded execution:

To run several Xvfb displays at the same time, you can use the `environ`
keyword when starting the `Xvfb` instances. This provides isolation between
threads. Be sure to use the environment dictionary you initialize Xvfb with
in your subsequent calls. Also, if you wish to inherit your current
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


class TestPages(unittest.TestCase):

    def setUp(self):
        xvfb = Xvfb()
        self.addCleanup(xvfb.stop)
        xvfb.start()
        self.driver = webdriver.Chrome()
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

## xvfbwrapper Development

Clone the repo:

```
git clone https://github.com/cgoldberg/xvfbwrapper.git
cd xvfbwrapper
```

Create a virtual env and install required testing packages:

```
python -m venv venv
source ./venv/bin/activate
pip install -r requirements_test.txt
```

Run all unit tests in the default Python environment:

```
pytest
```

Run all unit tests, linting, and type checking across all supported/installed
Python environments:

```
tox
```
