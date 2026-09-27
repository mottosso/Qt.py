## Caveats

There are cases where Qt.py is not handling incompatibility issues.

- [QtCore.QAbstractItemModel.createIndex](#qtcoreqabstractmodelcreateindex)
- [QtCore.QItemSelection](#qtcoreqitemselection)
- [QtCore.Slot](#qtcoreslot)
- [QtWidgets.QAction.triggered](#qtwidgetsqactiontriggered)
- [QtWidgets.qApp](#qtwidgetsqapp)
- [Fully Qualified Enums](#fully-qualified-enums)


<br>


**Tests**

Code blocks in this document are automatically tested at each commit before being accepted into the project. In order for your code to run successfully, follow these guidelines.

1. Each caveat MUST contain (1) a header, (2) description, (3) one or more examples and (4, optional) a solution.
1. Each caveat MUST have a header prefixed with four hashtags, e.g. `#### My Heading`.
1. Each example MAY target more than one binding at once by listing them comma-separated on the first line, e.g. `# PySide2, PyQt5`; the same example is then run once per listed binding. This is encouraged whenever the example applies identically to more than one binding.
1. Each example MUST visualise return value and any exceptions thrown.
1. An example MUST reside under a heading, e.g. `#### My Heading`
1. The first line of each example MUST be `# MyBinding`, where `MyBinding` is the binding you intend to test with, such as `PySide6` or `PyQt6`.
1. Examples MUST be in [doctest](https://docs.python.org/3.13/library/doctest.html) format. See other caveats for samples.
1. Examples MUST `import Qt` (where appropriate), NOT e.g. `import PyQt5`.
1. Examples MAY include `untested` in which case the continuous integration mechanism will look the other way, e.g. `# PyQt6, untested`
1. Examples MAY include `qapp` in which case a `QApplication` is created (reusing one if it already exists) before the example runs, e.g. `# PyQt5, qapp`. Note `QApplication.exit()` does not destroy the singleton, so a `QApplication` created by any test (tagged `qapp` or not) persists for the rest of the process; any example that creates its own must reuse an existing instance (`QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)`) rather than assuming none exists yet.
1. Ellipsis (...) can be used as a wildcard for return text checking, e.g. `AttributeError: type ...`.


<br>


#### QtGui.QAbstractItemModel.createIndex

In PySide2/6, if the last argument (the id) a Overflow error is raised. While in PyQt5/6 it gets coerced into an undefined unsigned value.

```python
# PySide2, PySide6
>>> from Qt import QtGui
>>> model = QtGui.QStandardItemModel()
>>> index = model.createIndex(0, 0, -1)
Traceback (most recent call last):
...
OverflowError: can't convert negative int to unsigned
```

```python
# PyQt5, PyQt6
>>> from Qt import QtGui
>>> model = QtGui.QStandardItemModel()
>>> index = model.createIndex(0, 0, -1)
>>> int(index.internalId()) == 18446744073709551615
True
```

##### Usecase

I had been using the id as an index into a list. But the unexpected return value from PyQt4 broke it by being invalid. The workaround was to always check that the returned id was between 0 and the max size I expect.  

\- @justinfx


<br>


#### QtCore.QItemSelection

PySide2/6 has the `QItemSelection.isEmpty` and `QItemSelection.empty` attributes while PyQt5/6 only has the `QItemSelection.isEmpty` attribute.

```python
# PySide2, PySide6
>>> from Qt import QtCore
>>> func = QtCore.QItemSelection.isEmpty
>>> func = QtCore.QItemSelection.empty
```

```python
# PyQt5, PyQt6
>>> from Qt import QtCore
>>> func = QtCore.QItemSelection.isEmpty
>>> func = QtCore.QItemSelection.empty
Traceback (most recent call last):
...
AttributeError: type object 'QItemSelection' has no attribute 'empty'...
```

##### Workaround

They both support the `len(selection)` operation.

```python
# PySide2, PySide6, PyQt5, PyQt6
>>> from Qt import QtCore
>>> selection = QtCore.QItemSelection()
>>> len(selection)
0
```


<br>


#### QtCore.Slot

PySide2/6 allows for a `result=None` keyword param to set the return type. PyQt5/6 crashes:

```python
# PySide2, PySide6
>>> from Qt import QtCore, QtWidgets
>>> slot = QtCore.Slot(QtWidgets.QWidget, result=None)
```

```python
# PyQt5, PyQt6
>>> from Qt import QtCore, QtWidgets
>>> slot = QtCore.Slot(QtWidgets.QWidget)
>>> slot = QtCore.Slot(QtWidgets.QWidget, result=None)
Traceback (most recent call last):
...
TypeError: bytes or ASCII string expected not 'NoneType'
```


<br>


#### QtWidgets.QAction.triggered

PySide2/6 cannot accept any arguments. In PyQt5/6, `QAction.triggered` signal can be passed arguments and doesn't return anything.

```python
# PySide2, PySide6, qapp
>>> from Qt import QtCore, QtWidgets
>>> obj = QtCore.QObject()
>>> action = QtWidgets.QAction(obj)
>>> action.triggered.emit()  # Note the return value (!)
True
>>> action.triggered.emit(True)
Traceback (most recent call last):
...
TypeError: triggered() only accepts 0 argument(s), 1 given!
```

```python
# PyQt5, PyQt6, qapp
>>> from Qt import QtCore, QtWidgets
>>> obj = QtCore.QObject()
>>> action = QtWidgets.QAction(obj)
>>> action.triggered.emit()
>>> action.triggered.emit(True)
```


<br>


#### QtWidgets.qApp

`qApp` is not included in Qt.py due to the way Qt keeps this up to date with the currently active QApplication.

Qt implicitly updates this variable through monkey patching whenever a new QApplication is instantiated. This means that our variable quickly goes out of date and is not updated at the same time.

```python
# PySide2, PySide6, PyQt5, PyQt6
>>> from Qt import QtWidgets
>>> "qApp" in dir(QtWidgets)
False
```

##### Workaround

Use `QApplication.instance()` instead.

Technically, there is no difference between the two, apart from more characters to type.

```python
# PySide2, PySide6, PyQt5, PyQt6, untested
>>> from Qt import QtWidgets
>>> app = QtWidgets.QApplication(sys.argv)
>>> app == QtWidgets.QApplication.instance()
True
```

Note: this workaround is marked untested to prevent issues with the `qapp` marker. This test explicitly shows the creation of the instance instead of using `QApplication.instance()`.


<br>


#### Fully Qualified Enums

In Qt6 both PySide6 and PyQt6 are moving from custom Enum classes to python Enums.
This means you should be moving from short form Enums `QFont.Bold` to
fully qualified Enum names `QFont.Weight.Bold`.

PySide6 currently has a [forgiveness mode](https://doc.qt.io/qtforpython-6/considerations.html#doing-a-smooth-transition-from-the-old-enums) where you can still use `QFont.Bold`
on a Qt class object but no longer let you use `QFont().Bold` on a instance of the
class. PyQt6 doesn't let you use either of these options and you must use the fully
qualified Enum name `QFont.Weight.Bold`.

There have already been a few short enum name conflicts introduced. `QtGui.QColorSpace`
for example has the enums `QColorSpace.NamedColorSpace.AdobeRgb` with a value of
3 and `QColorSpace.Primaries.AdobeRgb` with a value of 2. The value doesn't match
so you may not be passing the value you expect when using short enums. You can use
the `--show dups` mode of [Qt_convert_enum.py](/Qt_convert_enum.py) to generate a listing of duplicates
currently found in PySide6.

PySide, PyQt4 and older releases of PySide2 and PyQt5 can only use short enums
and are not compatible with fully qualified enum names. If you need to support Qt4
and Qt5 then use short enum's. You should also limit to `Qt.py<2`. Unfortunately
your code won't easily work with PyQt6.

For maximum compatibility with Qt5 and Qt6 moving forward, you should always use
the fully qualified enum name. Even if you only plan to support PySide2/6 you are
encouraged to use the fully qualified names for future proofing.

To convert existing code from short to fully qualified enum names use the
[Qt_convert_enum.py](/Qt_convert_enum.py) script included with Qt.py.

```bash
$ pip3 install Qt.py PySide2
$ python3 .../Qt_convert_enum.py /path/to/code/directory/to/update
```
This will search every .py file in the directory recursively and list any short
enums that need replaced in each file.

To actually update the code add `--write` flag. This updates existing files and
does not make backups of the existing files, so make sure to do that first.

To check for enum use regression you can add `--check`. This will change the return
code to the number of enums that require changing. A return code of zero indicates
that no enum changes are required. This check can only find and fix code that
is directly using enums on Qt class names. If you used `self.EnumName` or other
methods of accessing the enum objects the `--partial` check may find them. This is
unable to automatically fix your code but shows you possible code that you will
need to manually fix.
