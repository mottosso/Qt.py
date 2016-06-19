## Caveats

There are cases where Qt.py is not handling incompatibility issues.

- [Closures](CAVEATS.md#Closures)
- [QtCore.QAbstractModel.createIndex](CAVEATS.md#QtCore.QAbstractModel.createIndex)
- [QtCore.QItemSelection](CAVEATS.md#QtCore.QItemSelection)
- [QtCore.Slot](CAVEATS.md#QtCore.Slot)
- [QtGui.QRegExpValidator](CAVEATS.md#QtGui.QRegExpValidator)
- [QtWidgets.QAction.triggered](CAVEATS.md#QtWidgets.QAction.triggered)

<br>
<br>
<br>

#### Closures

```python 
# valid in PySide
def someMethod(self):
    def _wrapper():
        self.runSomething("foo")

    someObject._callback = _wrapper
    someObject.someSignal.connect(_wrapper)

# In PyQt4 an exception is generated when the signal fires
    def _wrapper():
        self.runSomething("foo")
NameError: free variable 'self' referenced before assignment in enclosing scope
```

<br>
<br>
<br>


#### QtCore.QAbstractModel.createIndex

In PySide, somehow the last argument (the id) is allowed to be negative and is maintained. While in PyQt4 it gets coerced into an undefined unsigned value.

```python
# PySide
>>> idx = model.createIndex(0, 0, -1)
>>> print idx.internalId()
# -1

# PyQt4
>>> idx = model.createIndex(0, 0, -1)
>>> print idx.internalId()
# 18446744073709551615
```

> Note - I had been using the id as an index into a list. But the unexpected return value from PyQt4 broke it by being invalid. The workaround was to always check that the returned id was between 0 and the max size I expect.  
– @justinfx

<br>
<br>
<br>

#### QtCore.QItemSelection

```python
# PySide
>>> QtGui.QItemSelection.empty()

# PyQt4
>>> QtGui.QItemSelection.isEmpty()
```

However, they both do support the len(selection) operation.

<br>
<br>
<br>

#### QtCore.Slot

PySide allows for a `result=None` keyword param to set the return type. PyQt4 crashes:

```python
>>> QtCore.Slot(QtGui.QWidget, result=None)
TypeError: string or ASCII unicode expected not 'NoneType'
```

<br>
<br>
<br>

#### QtGui.QRegExpValidator

In PySide, the constructor for `QtGui.QRegExpValidator()` can just take a `QRegExp` instance, and that is all.

In PyQt4 you are required to pass some form of a parent argument, otherwise you get a TypeError:

```python
QtGui.QRegExpValidator(regex, None)
```

<br>
<br>
<br>


#### QtWidgets.QAction.triggered

`QAction.triggered` signal requires a bool arg in PyQt4, while PySide cannot accept any arguments.

```python
# PySide
>>> a.triggered.emit()
>>> a.triggered.emit(True)
TypeError: triggered() only accept 0 arguments, 2 given!

# PyQt4
>>> a.triggered.emit()
TypeError: triggered(bool) has 1 argument(s) but 0 provided

>>> a.triggered.emit(True)  # is checked
```
