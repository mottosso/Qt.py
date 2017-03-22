[![Build Status](https://travis-ci.org/mottosso/Qt.py.svg?branch=master)](https://travis-ci.org/mottosso/Qt.py) [![PyPI version](https://badge.fury.io/py/Qt.py.svg)](https://pypi.python.org/pypi/Qt.py)

### Qt.py

Qt.py enables you to write software that runs on any of the 4 supported bindings - PySide2, PyQt5, PySide and PyQt4.

<br>

##### News

| Date     | Version   | Event
|:---------|:----------|:----------
| Mar 2017 | [1.0.0][] | Increased safety, **backwards incompatible**
| Sep 2016 | [0.6.9][] | Stable release
| Sep 2016 | [0.5.0][] | Alpha release of `--convert`
| Jun 2016 | [0.2.6][] | First release of Qt.py

- [More details](https://github.com/mottosso/Qt.py/releases).

[0.2.6]: https://github.com/mottosso/Qt.py/releases/tag/0.2.6
[0.5.0]: https://github.com/mottosso/Qt.py/releases/tag/0.5.0
[0.6.9]: https://github.com/mottosso/Qt.py/releases/tag/0.6.9
[1.0.0]: https://github.com/mottosso/Qt.py/releases/tag/1.0.0

##### Guides

- [Developing with Qt.py](https://fredrikaverpil.github.io/2016/07/25/developing-with-qt-py/)
- [Dealing with Maya 2017 and PySide2](https://fredrikaverpil.github.io/2016/07/25/dealing-with-maya-2017-and-pyside2/)
- [Udemy Course](https://www.udemy.com/python-for-maya/learn/v4/t/lecture/6027394)

##### Table of contents

- [Project goals](#project-goals)
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

### Project goals

Write once, run in any binding.

Qt.py was born in the film and visual effects industry to address the growing need for software capable of running with more than one flavor of the Qt bindings for Python - PySide, PySide2, PyQt4 and PyQt5.

| Goal                                 | Description
|:-------------------------------------|:---------------
| *Support co-existence*               | Qt.py should not affect other bindings running in same interpreter session.
| *Build for one, run with all*        | Code written with Qt.py should run on any binding.
| *Explicit is better than implicit*   | Differences between bindings should be visible to you.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for more details.

<br>
<br>
<br>

### Install

Qt.py is a single file and can either be [copy/pasted](https://raw.githubusercontent.com/mottosso/Qt.py/master/Qt.py) into your project, [downloaded](https://github.com/mottosso/Qt.py/archive/master.zip) as-is, cloned as-is or installed via PyPI.

```bash
$ pip install Qt.py
```

- Pro tip: Supports vendoring

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

- Also see [/examples](examples)

<br>
<br>
<br>

### Documentation

All members of `Qt` stem directly from those available via PySide2, along with these additional members.

| Attribute               | Returns     | Description
|:------------------------|:------------|:------------
| `__version__`           | `str`       | Version of this project
| `__binding__`           | `str`       | A string reference to binding currently in use
| `__qt_version__`        | `str`       | Reference to version of Qt, such as Qt 5.6.1
| `__binding_version__`   | `str`       | Reference to version of binding, such as PySide 1.2.6

**Example**

```python
>>> from Qt import __binding__
>>> __binding__
'PyQt5'
```

Qt.py also provides compatibility wrappers for critical functionality that differs across bindings, these can be found in the added `QtCompat` submodule.

| Attribute               | Returns     | Description
|:------------------------|:------------|:------------
| `load_ui(fname=str)`    | `QObject`   | Minimal wrapper of PyQt4.loadUi and PySide equivalent
| `translate(...)`        | `function`  | Compatibility wrapper around [QCoreApplication.translate][]
| `setSectionResizeMode()`| `method`    | Compatibility wrapper around [QAbstractItemView.setSectionResizeMode][]

[QCoreApplication.translate]: https://doc.qt.io/qt-5/qcoreapplication.html#translate
[QAbstractItemView.setSectionResizeMode]: https://doc.qt.io/qt-5/qheaderview.html#setSectionResizeMode

**Example**

```python
>>> from Qt import QtCompat
>>> QtCompat.setSectionResizeMode
```

<br>

##### Environment Variables

These are the publicly facing environment variables that in one way or another affect the way Qt.py is run.

| Variable             | Type  | Description
|:---------------------|:------|:----------
| QT_PREFFERED_BINDING | str   | Override order and content of binding to try.
| QT_VERBOSE           | bool  | Be a little more chatty about what's going on with Qt.py

<br>

##### Subset

Members of Qt.py is a subset of PySide2. Which means for a member to be made accessible via Qt.py, it will need to (1) be accessible via PySide2 and (2) each of the other supported bindings. This excludes large portions of the Qt framework, including the newly added QtQml and QtQuick modules but guarantees that anything you develop with Qt.py will work identically on any binding - PySide, PySide2, PyQt4 and PyQt5.

The version of PySide2 used as reference is the one specified on [VFX Platform](http://www.vfxplatform.com/). Currently version is 2.0.0.

<br>

##### Branch binding-specific code

Some bindings offer features not available in others, you can use `__binding__` to capture those.

```python
if "PySide" in __binding__:
  do_pyside_stuff()
```

<br>

##### Override preferred choice

If your system has multiple choices where one or more is preferred, you can override the preference and order in which they are tried with this environment variable.

```bash
$ set QT_PREFERRED_BINDING=PyQt5  # Windows
$ export QT_PREFERRED_BINDING=PyQt5  # Unix/OSX
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

##### Compile Qt Designer files

> WARNING - ALPHA FUNCTIONALITY<br>
> See [#132](https://github.com/mottosso/Qt.py/pull/132) for details.

`.ui` files compiled via `pyside2-uic` inherently contain traces of PySide2 - e.g. the line `from PySide2 import QtGui`.

In order to use these with Qt.py, or any other binding, one must first erase such traces and replace them with cross-compatible code.

```bash
$ pyside2-uic my_ui.ui -o my_ui.py
$ python -m Qt --convert my_ui.py
# Creating "my_ui_backup.py"..
# Successfully converted "my_ui.py"
```

Now you may use the file as you normally would, with Qt.py

<br>

##### Load Qt Designer files

The `uic.loadUi` function of PyQt4 and PyQt5 as well as the `QtUiTools.QUiLoader().load` function of PySide/PySide2 are mapped to a convenience function `load_ui`.

```python
import sys
from Qt import QtCompat

app = QtWidgets.QApplication(sys.argv)
ui = QtCompat.load_ui(fname="my.ui")
ui.show()
app.exec_()
```

Please note, `load_ui` has only one argument, whereas the PyQt and PySide equivalent has more. See [here](https://github.com/mottosso/Qt.py/pull/81) for details - in a nutshell, those arguments differ between PyQt and PySide in incompatible ways.

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

**Caveats**

There are cases where Qt.py is not handling incompatibility issues. Please see [`CAVEATS.md`](CAVEATS.md) for more information.

<br>
<br>
<br>

### Known Problems

Send us a pull-request with known problems here!

- [Maya and incompatible bindings on PYTHONPATH](https://github.com/mottosso/Qt.py/issues/146)

<br>
<br>
<br>

### Who's using Qt.py?

Send us a pull-request with your studio here.

- [Atomic Fiction](http://www.atomicfiction.com/)
- [Industrial Brothers](http://industrialbrothers.com/)
- [Moonbot Studios](http://moonbotstudios.com/)
- [Sony Pictures Imageworks](http://www.imageworks.com/)
- [Colorbleed](http://www.colorbleed.nl/)
- [Method Studios](http://www.methodstudios.com/)
- [Framestore](https://framestore.com)
- [Weta Digital](https://www.wetafx.co.nz/)
- [Disney Animation](https://www.disneyanimation.com/)
- [Industriromantik](http://www.industriromantik.se/)
- [Psyop](http://www.psyop.com/)
- [ftrack](https://www.ftrack.com/)
- [Fido](http://fido.se/)
- [Bläck](http://www.blackstudios.se/)
- [CGRU](http://cgru.info/)
- [MPC](http://www.moving-picture.com)
- [Rising Sun Pictures](https://rsp.com.au)

Presented at Siggraph 2016, BOF!

![image](https://cloud.githubusercontent.com/assets/2152766/17621229/c2448db2-6089-11e6-915f-0604e5d8c7ee.png)

<br>
<br>
<br>

### Projects using Qt.py

Send us a pull-request with your project here.

- [maya-capture-gui](https://github.com/BigRoy/maya-capture-gui)
- [pyblish-lite](https://github.com/pyblish/pyblish-lite)
- [pyvfx-boilerplate](https://github.com/fredrikaverpil/pyvfx-boilerplate)
- [riffle](https://gitlab.com/4degrees/riffle)
- [cmt](https://github.com/chadmv/cmt)
- [PythonForMayaSamples](https://github.com/dgovil/PythonForMayaSamples)
- [Kraken](https://github.com/fabric-engine/Kraken)
- [AFANASY](http://cgru.info/afanasy/afanasy)

<br>
<br>
<br>

### Projects similar to Qt.py

Comparison matrix.

| Project       | Audience      | Reference binding | License   | PEP8 |Standalone | PyPI   | Co-existence
|:--------------|:--------------|:------------------|:----------|------|:----------|--------|--------------
| Qt.py         | Film          | PySide2           | MIT       | X    | X         | X      | X
| [jupyter][]   | Scientific    | N/A               | N/A       | X    |           |        |
| [QtPy][]      | Scientific    | N/A               | MIT       |      | X         | X      |
| [pyqode.qt][] | Scientific    | PyQt5             | MIT       | X    |           | X      |
| [QtExt][]     | Film          | N/A               | N/A       |      | X         |        |

Also worth mentioning, [pyqt4topyqt5](https://github.com/rferrazz/pyqt4topyqt5); a good starting point for transitioning to Qt.py.

Send us a pull-request with your project here.

[QtPy]: https://github.com/spyder-ide/qtpy
[jupyter]: https://github.com/jupyter/qtconsole/blob/master/qtconsole/qt_loaders.py
[pyqode.qt]: https://github.com/pyQode/pyqode.qt
[QtExt]: https://bitbucket.org/ftrack/qtext

<br>
<br>
<br>

### Developer Guide

Tests are performed on each aspect of the shim.

- [Functional](tests.py)
- [Caveats](build_caveats.py)
- [Examples](examples)
- [Membership](build_membership.py)

Each of these are run under..

- Python 2.7
- Python 3.4

..once for each binding or under a specific binding only.

Each test is run within it's own isolated process, so as to allow an `import` to occur independently from other tests. Process isolation is handled via [nosepipe](https://pypi.python.org/pypi/nosepipe).

Tests that are written at module level are run four times - once per binding - whereas tests written under a specific if-statement are run only for this particular binding.

```python
if binding("PyQt4"):
    def test_something_related_to_pyqt4():
        pass
```

**Running tests**

Due to the nature of multiple bindings and multiple interpreter support, setting up a development environment in which to properly test your contraptions can be challenging. So here is a guide for how to do just that using **Docker**.

With Docker setup, here's what you do.

```bash
# Build image
cd Qt.py
docker build -t mottosso/qt.py27 -f Dockerfile-py2.7 .
docker build -t mottosso/qt.py35 -f Dockerfile-py3.5 .

# Run nosetests (Linux/OSX)
docker run --rm -v $(pwd):/Qt.py mottosso/qt.py27
docker run --rm -v $(pwd):/Qt.py mottosso/qt.py35

# Run nosetests (Windows)
docker run --rm -v %CD%:/Qt.py mottosso/qt.py27
docker run --rm -v %CD%:/Qt.py mottosso/qt.py35

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

Now both you and Travis are operating on the same assumptions which means that when the tests pass on your machine, they pass on Travis. And everybody wins!

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for more of the good stuff.
