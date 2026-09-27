## `loadUi` examples

#### Base instance as argument

The `uic.loadUi` function of PyQt5 and PyQt6 as well as the `QtUiTools.QUiLoader().load` function of PySide2/PySide6 are mapped to a convenience function in Qt.py called `loadUi` (part of the `QtCompat` module; `QtCompat.loadUi`).

A popular approach is to provide a base instance argument to PyQt's `uic.loadUi`, into which all widgets are loaded:

```python
# PyQt5, PyQt6
class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi('uifile.ui', self)  # Loads all widgets of uifile.ui into self
```

PySide does not support this out of the box, but you can use `QtCompat.loadUi`.
