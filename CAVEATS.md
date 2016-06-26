## Caveats

There are cases where Qt.py is not handling incompatibility issues.

- [Closures](CAVEATS.md#closures)
- [QtCore.QAbstractModel.createIndex](CAVEATS.md#qtcoreqabstractmodelcreateindex)
- [QtCore.QItemSelection](CAVEATS.md#qtcoreqitemselection)
- [QtCore.Slot](CAVEATS.md#qtcoreslot)
- [QtGui.QRegExpValidator](CAVEATS.md#qtguiqregexpvalidator)
- [QtWidgets.QAction.triggered](CAVEATS.md#qtwidgetsqactiontriggered)

<br>
<br>

**Contribute your own caveat**

Pull-requests are welcome, here's how you can make yours.

Code blocks in file are automatically tested on before commited into the project. In order for your code to run successfully, follow these guidelines.

1. Each caveat MUST have a header prefixed with four (4) `#`, e.g. `#### My Heading`.
1. Each caveat SHOULD have example code.
1. Each caveat MAY have one or more example.
1. Each example MAY NOT use more than one (1) binding at a time, e.g. both PyQt5 and PySide.
1. Each example SHOULD `assert` what *is* working, along with what *isn't*.
1. An example MUST reside under a heading, e.g. `#### My Heading`
1. A heading MUST NOT contain anything but letters, numbers, spaces and dots.
1. The first line of each example MUST be `# MyBinding`, where `MyBinding` is the binding you intend to test with, such as `PySide` or `PyQt5`.
1. Examples MUST be in docstring format. See other caveats for samples.
1. Examples MUST `import Qt` (where appropriate), NOT e.g. `import PyQt5`.

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
>>> from Qt import QtCore
>>> assert not hasattr(QtCore.QItemSelection, "isEmpty")
>>> assert hasattr(QtCore.QItemSelection, "empty")
```

```python
# PyQt4
>>> from Qt import QtCore
>>> assert hasattr(QtCore.QItemSelection, "isEmpty")
>>> assert not hasattr(QtCore.QItemSelection, "empty")
```

However, they both do support the len(selection) operation.

<br>
<br>
<br>


#### QtCore.Slot

PySide allows for a `result=None` keyword param to set the return type. PyQt4 crashes:

```python
# PySide
>>> from Qt import QtCore, QtGui
>>> try:
...     assert isinstance(QtCore.Slot(QtGui.QWidget, result=None), QtCore.Slot)
... except TypeError:
...     assert False
```

```python
# PyQt4
>>> from Qt import QtCore, QtGui
>>> try:
...     assert not isinstance(QtCore.Slot(QtGui.QWidget, result=None), QtCore.Slot)
... except TypeError:
...     assert True
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
