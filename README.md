### qt

Python 2 &amp; 3 compatibility wrapper around all Qt bindings - PySide, PySide2, PyQt4 and PyQt5.

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
