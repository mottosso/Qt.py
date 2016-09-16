"""Map all bindings to PySide2

This module replaces itself with the most desirable binding.

Project goals:
    Qt.py was born in the film and visual effects industry to address
    the growing need for the development of software capable of running
    with more than one flavour of the Qt bindings for Python - PySide,
    PySide2, PyQt4 and PyQt5.

    1. Build for one, run with all
    2. Explicit is better than implicit
    3. Support co-existence

Default resolution order:
    - PySide2
    - PyQt5
    - PySide
    - PyQt4

Usage:
    >>> import sys
    >>> from Qt import QtWidgets
    >>> app = QtWidgets.QApplication(sys.argv)
    >>> button = QtWidgets.QPushButton("Hello World")
    >>> button.show()
    >>> app.exec_()

"""

import os
import sys

__version__ = "0.4.3"

# All unique members of Qt.py
__added__ = list()

# Members copied from elsewhere, such as QtGui -> QtWidgets
__remapped__ = list()

# Existing members modified in some way
__modified__ = list()


def remap(object, name, value, safe=True):
    """Prevent accidental assignment of existing members

    Arguments:
        object (object): Parent of new attribute
        name (str): Name of new attribute
        value (object): Value of new attribute
        safe (bool): Whether or not to guarantee that
            the new attribute was not overwritten.
            Can be set to False under condition that
            it is superseded by extensive testing.

    """

    if os.getenv("QT_TESTING") is not None and safe:
        # Cannot alter original binding.
        if hasattr(object, name):
            raise AttributeError("Cannot override existing name: "
                                 "%s.%s" % (object.__name__, name))

        # Cannot alter classes of functions
        if type(object).__name__ != "module":
            raise AttributeError("%s != 'module': Cannot alter "
                                 "anything but modules" % object)

    elif hasattr(object, name):
        # Keep track of modifications
        __modified__.append(name)

    if name not in __added__:
        __remapped__.append(name)

    setattr(object, name, value)


def add(object, name, value, safe=True):
    """Identical to :func:`remap` and provided for readability only"""
    __added__.append(name)
    remap(object, name, value, safe)


def pyqt5():
    import PyQt5.Qt
    from PyQt5 import QtCore, uic

    remap(QtCore, "Signal", QtCore.pyqtSignal)
    remap(QtCore, "Slot", QtCore.pyqtSlot)
    remap(QtCore, "Property", QtCore.pyqtProperty)

    add(PyQt5, "__wrapper_version__", __version__)
    add(PyQt5, "__binding__", "PyQt5")
    add(PyQt5, "__binding_version__", QtCore.PYQT_VERSION_STR)
    add(PyQt5, "__qt_version__", QtCore.QT_VERSION_STR, safe=False)
    add(PyQt5, "__added__", __added__)
    add(PyQt5, "__remapped__", __remapped__)
    add(PyQt5, "__modified__", __modified__)
    add(PyQt5, "load_ui", lambda fname: uic.loadUi(fname))

    return PyQt5


def pyqt4():
    # Attempt to set sip API v2 (must be done prior to importing PyQt4)
    import sip
    try:
        sip.setapi("QString", 2)
        sip.setapi("QVariant", 2)
        sip.setapi("QDate", 2)
        sip.setapi("QDateTime", 2)
        sip.setapi("QTextStream", 2)
        sip.setapi("QTime", 2)
        sip.setapi("QUrl", 2)
    except AttributeError:
        raise ImportError
        # PyQt4 < v4.6
    except ValueError:
        # API version already set to v1
        raise ImportError

    import PyQt4.Qt
    from PyQt4 import QtCore, QtGui, uic

    remap(PyQt4, "QtWidgets", QtGui)
    remap(QtCore, "Signal", QtCore.pyqtSignal)
    remap(QtCore, "Slot", QtCore.pyqtSlot)
    remap(QtCore, "Property", QtCore.pyqtProperty)
    remap(QtCore, "QItemSelection", QtGui.QItemSelection)
    remap(QtCore, "QStringListModel", QtGui.QStringListModel)
    remap(QtCore, "QItemSelectionModel", QtGui.QItemSelectionModel)
    remap(QtCore, "QSortFilterProxyModel", QtGui.QSortFilterProxyModel)
    remap(QtCore, "QAbstractProxyModel", QtGui.QAbstractProxyModel)

    try:
        from PyQt4 import QtWebKit
        remap(PyQt4, "QtWebKitWidgets", QtWebKit)
    except ImportError:
        # QtWebkit is optional in Qt , therefore might not be available
        pass

    add(PyQt4, "__wrapper_version__", __version__)
    add(PyQt4, "__binding__", "PyQt4")
    add(PyQt4, "__binding_version__", QtCore.PYQT_VERSION_STR)
    add(PyQt4, "__qt_version__", QtCore.QT_VERSION_STR)
    add(PyQt4, "__added__", __added__)
    add(PyQt4, "__remapped__", __remapped__)
    add(PyQt4, "__modified__", __modified__)
    add(PyQt4, "load_ui", lambda fname: uic.loadUi(fname))

    return PyQt4


def pyside2():
    import PySide2
    from PySide2 import QtGui, QtCore, QtUiTools

    remap(QtCore, "QStringListModel", QtGui.QStringListModel)

    add(PySide2, "__wrapper_version__", __version__)
    add(PySide2, "__binding__", "PySide2")
    add(PySide2, "__binding_version__", PySide2.__version__)
    add(PySide2, "__qt_version__", PySide2.QtCore.qVersion())
    add(PySide2, "__added__", __added__)
    add(PySide2, "__remapped__", __remapped__)
    add(PySide2, "__modified__", __modified__)
    add(PySide2, "load_ui", lambda fname: QtUiTools.QUiLoader().load(fname))

    return PySide2


def pyside():
    import PySide
    from PySide import QtGui, QtCore, QtUiTools

    remap(PySide, "QtWidgets", QtGui)
    remap(QtCore, "QSortFilterProxyModel", QtGui.QSortFilterProxyModel)
    remap(QtCore, "QStringListModel", QtGui.QStringListModel)
    remap(QtCore, "QItemSelection", QtGui.QItemSelection)
    remap(QtCore, "QItemSelectionModel", QtGui.QItemSelectionModel)
    remap(QtCore, "QAbstractProxyModel", QtGui.QAbstractProxyModel)

    try:
        from PySide import QtWebKit
        remap(PySide, "QtWebKitWidgets", QtWebKit)
    except ImportError:
        # QtWebkit is optional in Qt , therefore might not be available
        pass

    add(PySide, "__wrapper_version__", __version__)
    add(PySide, "__binding__", "PySide")
    add(PySide, "__binding_version__", PySide.__version__)
    add(PySide, "__qt_version__", PySide.QtCore.qVersion())
    add(PySide, "__added__", __added__)
    add(PySide, "__remapped__", __remapped__)
    add(PySide, "__modified__", __modified__)
    add(PySide, "load_ui", lambda fname: QtUiTools.QUiLoader().load(fname))

    return PySide


def log(text, verbose):
    if verbose:
        sys.stdout.write(text)


def init():
    """Try loading each binding in turn

    Please note: the entire Qt module is replaced with this code:
        sys.modules["Qt"] = binding()

    This means no functions or variables can be called after
    this has executed.

    """

    preferred = os.getenv("QT_PREFERRED_BINDING")
    verbose = os.getenv("QT_VERBOSE") is not None
    bindings = (pyside2, pyqt5, pyside, pyqt4)

    if preferred:
        # Internal flag (used in installer)
        if preferred == "None":
            sys.modules[__name__].__wrapper_version__ = __version__
            return

        preferred = preferred.split(os.pathsep)
        available = {
            "PySide2": pyside2,
            "PyQt5": pyqt5,
            "PySide": pyside,
            "PyQt4": pyqt4
        }

        try:
            bindings = [available[binding] for binding in preferred]
        except KeyError:
            raise ImportError(
                "Available preferred Qt bindings: "
                "\n".join(preferred)
            )

    for binding in bindings:
        log("Trying %s" % binding.__name__, verbose)

        try:
            binding = binding()

        except ImportError as e:
            log(" - ImportError(\"%s\")\n" % e, verbose)
            continue

        else:
            # Reference to this module
            binding.__shim__ = sys.modules[__name__]

            sys.modules.update({
                __name__: binding,

                # Fix #133, `from Qt.QtWidgets import QPushButton`
                __name__ + ".QtWidgets": binding.QtWidgets

            })

            return

    # If not binding were found, throw this error
    raise ImportError("No Qt binding were found.")


init()
