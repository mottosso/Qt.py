### Qt

Python 2 and 3 compatibility wrapper around all Qt bindings - PySide, PySide2, PyQt4 and PyQt5.

<br>
<br>
<br>

### Install

```bash
$ pip install Qt
```

<br>
<br>
<br>

### Usage

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

### How it works

This wrapper provides a common interface around all available Python bindings for Qt by adhering to the interface of PySide2 and mapping everything that differs into that interface.

**Example**

```python
if binding == "PySide":
    Qt.QtWidgets = Qt.QtGui
```


The idea is to map the parts that does not change - i.e. legacy code - to the parts that do - i.e. the latest version.

<br>
<br>
<br>

### Documentation

All members of `Qt` stem directly from those available via PySide2.

Here are a few additional members.

```python
import Qt

# A string reference to binding currently in use
Qt.__binding__ == "PyQt5"

# Reference to version of Qt, such as Qt 5.6.1
Qt.__qtVersion__ == (5, 6, 1)

# Reference to version of binding, such as PySide 1.2.6
Qt.__bindingVersion == (1, 2, 6)

# Version of this project
Qt.__version__ == "1.0.0"
```

> Additional members follow mixedCase rather than standard PEP08 snake_case, to remain similar to Qt and the bindings themselves.

<br>
<br>
<br>

### Contributing

To contribute, fork this project and submit a pull-request.

Your code will be reviewed and merged once it:

1. Does something useful
1. Is up to par with surrounding code

Development for this project takes place in individual forks. The parent project ever only contains a single branch, a branch containing the latest working version of the project.

Bugreports must include:

1. Description
2. Expected results
3. Short reproducible
 
Feature requests must include:

1. Goal (what the feature aims to solve)
2. Motivation (why *you* think this is necessary)
3. Suggested implementation (psuedocode)

Questions may also be submitted as issues.
