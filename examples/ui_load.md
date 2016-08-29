## `load_ui` examples

### Providing a base instance

The `uic.loadUi` function of PyQt4 and PyQt5 as well as the `QtUiTools.QUiLoader().load` function of PySide/PySide2 are mapped to a convenience function in Qt.py called `load_ui`.

This document outlines advanced usage of `load_ui`.

<br>
<br>
<br>


#### Base instance as argument using getattr/setattr

A popular approach is to provide a base instance argument to PyQt's `uic.loadUi`, into which all widgets are loaded:


    uic.loadUi('uifile.ui', self)
    self.my_widget


PySide does not support this out of the box, but it can be implemented in various ways. In the example below, a support function `setup_ui` is defined which wraps `load_ui` and provides this second base instance argument.

```python
# PySide
>>> from Qt import QtWidgets, load_ui
>>> 
>>> 
>>> def setup_ui(uifile, base_instance=None):
...     ui = load_ui(uifile)
...     if not base_instance:
...         return ui
...     else:
...         for member in dir(ui):
...             if not member.startswith('__') and member is not 'staticMetaObject':
...                 setattr(base_instance, member, getattr(ui, member))
...         return ui
>>> 
>>> 
>>> class MainWindow(QtWidgets.QWidget):
...     def __init__(self, parent=None):
...         QtWidgets.QWidget.__init__(self, parent)
...         setup_ui('examples/ui_load_qwidget.ui', self)
>>> 
>>> app = QtWidgets.QApplication(sys.argv)
>>> window = MainWindow()
>>> 
>>> 
>>> # Tests
>>> assert isinstance(window.__class__, type(QtWidgets.QWidget))
>>> assert isinstance(window.parent(), type(None))
>>> assert isinstance(window.lineEdit.__class__, type(QtWidgets.QWidget))
>>> assert window.lineEdit.text() == ''
>>> window.lineEdit.setText('Hello')
>>> assert window.lineEdit.text() == 'Hello'
>>> 
>>> app.exit()
```
