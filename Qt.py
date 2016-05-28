"""Importing this file means importing the most desireable bindings for
Qt relative the running version of Python.
"""

import sys

QT_BINDING_LOAD_ORDER = ['PySide2', 'PyQt5', 'PySide', 'PyQt4']


def load_pyqt5():
    """Load PyQt5 for Qt5 bindings"""
    import PyQt5.Qt
    sys.modules["Qt"] = PyQt5
    PyQt5.QtCore.Signal = PyQt5.QtCore.pyqtSignal
    PyQt5.QtCore.Slot = PyQt5.QtCore.pyqtSlot
    PyQt5.QtCore.Property = PyQt5.QtCore.pyqtProperty
    PyQt5.__binding__ = "PyQt5"


def load_pyqt4():
    """Load PyQt4 for Qt4 bindings"""
    import PyQt4.Qt
    sys.modules["Qt"] = PyQt4
    PyQt4.QtWidgets = PyQt4.QtGui
    PyQt4.QtCore.Signal = PyQt4.QtCore.pyqtSignal
    PyQt4.QtCore.Slot = PyQt4.QtCore.pyqtSlot
    PyQt4.QtCore.Property = PyQt4.QtCore.pyqtProperty
    PyQt4.__binding__ = "PyQt4"


def load_pyside2():
    """Load PySide2 for Qt5 bindings"""
    import PySide2
    sys.modules["Qt"] = PySide2
    PySide2.__binding__ = "PySide2"


def load_pyside():
    """Load PySide for Qt4 bindings"""
    import PySide
    from PySide import QtGui
    PySide.QtWidgets = QtGui
    PySide.QtCore.QSortFilterProxyModel = PySide.QtGui.QSortFilterProxyModel
    sys.modules["Qt"] = PySide
    PySide.__binding__ = "PySide"


def load_wrapper(function_name):
    """Load the function given and handle error messages"""
    try:
        exec function_name
        return True
    except ImportError:
        return False
    except NameError:
        sys.stderr.write('Qt: Function name, ' + function_name +
                         ' doesn\'t exist.\n')
        return False


loaded = False
for binding in QT_BINDING_LOAD_ORDER:
    if not loaded:
        function_name = 'load_' + binding.lower() + '()'
        loaded = load_wrapper(function_name)
if not loaded:
    sys.stderr.write("Qt: Could not find appropriate bindings for Qt\n")
