### Qt.py

Qt.py enables you to write software that dynamically chooses the most desireable bindings based on what's available, including PySide, PySide2, PyQt4 and PyQt5.

<br>
<br>
<br>

### Install

Qt.py is a single file and can either be downloaded as-is or installed via PyPI.

```bash
$ pip install Qt.py
```

<br>
<br>
<br>

### Usage

Use Qt.py as you would use PyQt5 or PySide2.

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

### Documentation

All members of `Qt` stem directly from those available via PySide2, along with these additional members.

```python
import Qt

# A string reference to binding currently in use
Qt.__binding__ == 'PyQt5'

# Reference to version of Qt, such as Qt 5.6.1
Qt.__qt_version__ == '5.6.1'

# Reference to version of binding, such as PySide 1.2.6
Qt.__binding_version__ == '1.2.6'

# Version of this project
Qt.__version__ == '1.0.0'
```

**Branch binding-specific code**

Some bindings offer features not available in others, you can use `__binding__` to capture those.

```python
if "PySide" in Qt.__binding__:
  do_pyside_stuff()
```

**Override preferred choice**

If your system has multiple choices, one of which is preferred, you can override the dynamic discovery mechanism with this environment variable.

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

<br>
<br>
<br>

### Known Problems

None yet.

<br>
<br>
<br>

### Projects using Qt.py

Send us a pull-request with your project here.

- https://github.com/pyblish/pyblish-lite
