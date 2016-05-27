### qt

Python 2 and 3 compatibility wrapper around all Qt bindings - PySide, PySide2, PyQt4 and PyQt5.

### Install

```bash
$ pip install qt
```

### Usage

```python
import sys
from Qt import QtWidgets

app = QtWidgets.QApplication(sys.argv)
button = QtWidgets.QPushButton("Hello World")
button.show()
app.exec_()
```

### How it works

This wrapper provides a common interface around all available Python bindings for Qt by adhering to the interface of PySide2 and mapping everything that differs into that interface.

**Example**

```python
if binding == "PySide":
    Qt.QtWidgets = Qt.QtGui
```


The idea is to map the parts that does not change - i.e. legacy code - to the parts that do - i.e. the latest version.

