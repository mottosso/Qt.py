"""Importing this file means importing the most desireable bindings for
Qt relative the running version of Python.
"""

import sys


def load_pyqt5():
    """Load PyQt5 for Qt5 bindings"""
    try:
        import PyQt5.Qt
        sys.modules["Qt"] = PyQt5
        PyQt5.QtCore.Signal = PyQt5.QtCore.pyqtSignal
        PyQt5.QtCore.Slot = PyQt5.QtCore.pyqtSlot
        PyQt5.QtCore.Property = PyQt5.QtCore.pyqtProperty
        PyQt5.__binding__ = "PyQt5"
        return True
    except ImportError:
        return False


def load_pyqt4():
    """Load PyQt4 for Qt4 bindings"""
    try:
        import PyQt4.Qt
        sys.modules["Qt"] = PyQt4
        PyQt4.QtWidgets = PyQt4.QtGui
        PyQt4.QtCore.Signal = PyQt4.QtCore.pyqtSignal
        PyQt4.QtCore.Slot = PyQt4.QtCore.pyqtSlot
        PyQt4.QtCore.Property = PyQt4.QtCore.pyqtProperty
        PyQt4.__binding__ = "PyQt4"
        return True
    except ImportError:
        return False


def load_pyside2():
    """Load PySide2 for Qt5 bindings"""
    try:
        import PySide2
        sys.modules["Qt"] = PySide2
        PySide2.__binding__ = "PySide2"
        return True
    except ImportError:
        return False


def load_pyside():
    """Load PySide for Qt4 bindings"""
    try:
        import PySide
        from PySide import QtGui
        PySide.QtWidgets = QtGui
        PySide.QtCore.QSortFilterProxyModel = PySide.QtGui.QSortFilterProxyModel
        sys.modules["Qt"] = PySide
        PySide.__binding__ = "PySide"
        return True
    except ImportError:
        return False


if load_pyside2():
    pass
elif load_pyqt5():
    pass
elif load_pyside():
    pass
elif load_pyqt4():
    pass
else:
    sys.stderr.write("Qt: Could not find appropriate bindings for Qt\n")
