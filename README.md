[![Build Status](https://travis-ci.org/mottosso/Qt.py.svg?branch=master)](https://travis-ci.org/mottosso/Qt.py)

### Qt.py

Qt.py enables you to write software that dynamically chooses the most desireable bindings based on what's available, including PySide2, PyQt5, PySide and PyQt4; in that (configurable) order (see below).

**Guides**

- [Developing with Qt.py](https://fredrikaverpil.github.io/2016/07/25/developing-with-qt-py/)
- [Dealing with Maya 2017 and PySide2](https://fredrikaverpil.github.io/2016/07/25/dealing-with-maya-2017-and-pyside2/)

**Table of contents**

- [Install](#install)
- [Usage](#usage)
- [Documentation](#documentation)
- [Rules](#rules)
- [How it works](#how-it-works)
- [Known problems](#known-problems)
- [Who's using Qt.py?](#whos-using-qtpy)
- [Projects using Qt.py](#projects-using-qtpy)
- [Projects similar to Qt.py](#projects-similar-to-qtpy)
- [Developer guide](#developer-guide)

<br>
<br>
<br>

### Development goals

Qt.py was born in the film and visual effects industry to address the growing needs for the development of software capable of running with more than one flavour of the Qt bindings for Python - PySide, PySide2, PyQt4 and PyQt5.

1. **Support co-existence** - Qt.py should not affect other bindings running in same interpreter session.
1. **Don't get smart** - One file, copy/paste installation, keep it simple.
1. **No bugs** - No implementations = No bugs.

See [`CONTRIBUTING.md`](blob/master/CONTRIBUTING.md) for more details.

<br>
<br>
<br>

### Install

Qt.py is a single file and can either be [copy/pasted](https://raw.githubusercontent.com/mottosso/Qt.py/master/Qt.py) into your project, [downloaded](https://github.com/mottosso/Qt.py/archive/master.zip) as-is or installed via PyPI.

```bash
$ pip install Qt.py
```

<br>
<br>
<br>

### Usage

Use Qt.py as you would use PySide2.

![image](https://cloud.githubusercontent.com/assets/2152766/15653248/b5ce298e-2683-11e6-8c0c-f041ecae203d.png)

```python
import sys
from Qt import QtWidgets

app = QtWidgets.QApplication(sys.argv)
button = QtWidgets.QPushButton("Hello World")
button.show()
app.exec_()
```

<br>
<br>
<br>

### Documentation

All members of `Qt` stem directly from those available via PySide2, along with these additional members.

| Attribute               | Type   | Value
|:------------------------|:-------|:------------
| `__binding__`           | `str`  | A string reference to binding currently in use
| `__qt_version__`        | `str`  | Reference to version of Qt, such as Qt 5.6.1
| `__binding_version__`   | `str`  | Reference to version of binding, such as PySide 1.2.6
| `__wrapper_version__`   | `str`  | Version of this project
| `load_ui()`             | `func` | Minimal wrapper of PyQt4.loadUi and PySide equivalent

<br>

##### Branch binding-specific code

Some bindings offer features not available in others, you can use `__binding__` to capture those.

```python
if "PySide" in Qt.__binding__:
  do_pyside_stuff()
```

<br>

##### Override preferred choice

If your system has multiple choices where one or more is preferred, you can override the preference and order in which they are tried with this environment variable.

```bash
# Windows
$ set QT_PREFERRED_BINDING=PyQt5
$ python -c "import Qt;print(Qt.__binding__)"
PyQt5

# Unix/OSX
$ export QT_PREFERRED_BINDING=PyQt5
$ python -c "import Qt;print(Qt.__binding__)"
PyQt5
```

Constrain available choices and order of discovery by supplying multiple values.

```bash
# Try PyQt first and then PySide, but nothing else.
$ export QT_PREFERRED_BINDING=PyQt:PySide
```

Using the OS path separator (`os.pathsep`) which is `:` on Unix systems and `;` on Windows.

<br>

##### Load Qt Designer .ui files

The `uic.loadUi` function of PyQt4 and PyQt5 as well as the `QtUiTools.QUiLoader().load` function of PySide/PySide2 are mapped to a convenience function `load_ui`.

```python
import sys
import Qt

app = QtWidgets.QApplication(sys.argv)
ui = Qt.load_ui("my.ui")
ui.show()
app.exec_()
```

Please note, for maximum compatibility, only pass the argument of the filename to the `load_ui` function.

<br>

##### sip API v2

If you're using PyQt4, `sip` attempts to set its API to version 2 for the following:
- `QString`
- `QVariant`
- `QDate`
- `QDateTime`
- `QTextStream`
- `QTime`
- `QUrl`

<br>
<br>
<br>

### Rules

The PyQt and PySide bindings are similar, but not identical. Where there is ambiguity, there must to be a clear direction on which path to take.

**Governing API**

The official [Qt 5 documentation](http://doc.qt.io/qt-5/classes.html) is always right. Where the documentation lacks answers, PySide2 is right.

For example.

```python
# PyQt5 adheres to PySide2 signals and slots
PyQt5.Signal = PyQt5.pyqtSignal
PyQt5.Slot = PyQt5.pyqtSlot

# PySide2 adheres to the official documentation
PySide2.QtCore.QStringListModel = PySide2.QtGui.QStringListModel
```

**Portability**

Qt.py does not hide members from the original binding. This can be problematic if, for example, you accidentally use a member that only exists PyQt5 and later try running your software with a different binding.

```python
from Qt import QtCore

# Incompatible with PySide
signal = QtCore.pyqtSignal()
```

But it enables use of Qt.py as a helper library, in conjunction with an existing binding, simplifying the transition of an existing project from a particular binding.

```python
# This is ok
from Qt import QtCore
from PyQt4 import QtGui
```

**Caveats**

There are cases where Qt.py is not handling incompatibility issues. Please see [`CAVEATS.md`](CAVEATS.md) for more information.

<br>
<br>
<br>

### How it works

Once you import Qt.py, Qt.py replaces itself with the most desirable binding on your platform, or throws an `ImportError` if none are available.

```python
>>> import Qt
>>> print(Qt)
<module 'PyQt5' from 'C:\Python27\lib\site-packages\PyQt5\__init__.pyc'>
```

Here's an example of how this works.

**Qt.py**

```python
import sys
import PyQt5

# Replace myself PyQt5
sys.modules["Qt"] = PyQt5
```

Once imported, it is as though your application was importing whichever binding was chosen and Qt.py never existed.

<br>
<br>
<br>

### Known Problems

None yet.

<br>
<br>
<br>

### Who's using Qt.py?

Send us a pull-request with your studio here.

- Framestore
- Weta Digital
- Disney Animation
- Industriromantik

Presented at Siggraph 2016, BOF!

![image](https://cloud.githubusercontent.com/assets/2152766/17621229/c2448db2-6089-11e6-915f-0604e5d8c7ee.png)

<br>
<br>
<br>

### Projects using Qt.py

Send us a pull-request with your project here.

- https://github.com/pyblish/pyblish-lite
- https://github.com/fredrikaverpil/pyvfx-boilerplate
- https://gitlab.com/4degrees/riffle

<br>
<br>
<br>

### Projects similar to Qt.py

Send us a pull-request with your project here.

- https://github.com/spyder-ide/qtpy
- https://github.com/jupyter/qtconsole/blob/master/qtconsole/qt_loaders.py

<br>
<br>
<br>

### Developer Guide

Due to the nature of multiple bindings and multiple interpreter support, setting up a development environment in which to properly test your contraptions can be challenging. So here is a guide for how to do just that using **Docker**.

This project uses Travis for continuous integration and Travis uses Ubuntu 14.04. For an ideal development environment, we'd better stick with it. There is one more advantage to using the same environment, which I will show you.

Assuming you have Docker already setup.

```bash
# Build image (see Dockerfile for specifics)
cd Qt.py
docker build -t mottosso/qt.py27 -f Dockerfile-py2.7 .
docker build -t mottosso/qt.py35 -f Dockerfile-py3.5 .

# Run nosetests
# Explanation of flags:
# --rm 	delete the container on exit
# -v 	mount local path to container path
docker run --rm -v $(pwd):/Qt.py mottosso/qt.py27
docker run --rm -v $(pwd):/Qt.py mottosso/qt.py35

# Doctest: test_caveats.test_1_qtgui_qabstractitemmodel_createindex ... ok
# Doctest: test_caveats.test_2_qtgui_qabstractitemmodel_createindex ... ok
# Doctest: test_caveats.test_3_qtcore_qitemselection ... ok
# ...
#
# ----------------------------------------------------------------------
# Ran 21 tests in 7.799s
# 
# OK
```

The dependencies, and OS, can and should be identical to those found in [`.travis.yml`](https://github.com/mottosso/Qt.py/blob/master/.travis.yml). That way, both you and Travis are operating on the same assumptions which means that when the tests pass on your machine, they pass on Travis. And everybody wins!

**Commits**

Commits should be well contained, as small as possible (but no smaller) and its messages should be in present-tense, imperative-style.

E.g.

```bash
# No
Changed this and did that

# No
Changes this and does that

# Yes
Change this and do that
```

The reason is that, each commit is like an action. An event. And it is perfectly possible to "cherry-pick" a commit onto any given branch. In this style, it makes more sense what exactly the commit will do to your code.

- Cherry pick "Add this and remove that"
- Cherry pick "Remove X and replace with Y"

**Version bumping**

This project uses [semantic versioning](http://semver.org/) and is updated *after* a new release has been made.

For example, if the project had 100 commits at the time of the latest release and has 103 commits now, then it's time to increment. If however you modify the project and it has not yet been released, then your changes are included in the overall next release.

The goal is to make a new release per increment.

**Making a Release**

Once the project has gained features, had bugs sorted out and is in a relatively stable state, it's time to make a new release.

- https://github.com/mottosso/Qt.py/releases

Each release should come with:

- An short summary of what has changed.
- A full changelog, including links to resolved issues.
 
The release is then automatically uploaded to PyPI.

```bash
$ pip install Qt.py
```
