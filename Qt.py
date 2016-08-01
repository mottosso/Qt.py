"""Map all bindings to PySide2

This module replaces itself with the most desirable binding.

Resolution order:
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

__version__ = "0.3.2"


def _pyqt5():
    import PyQt5.Qt

    # Remap
    PyQt5.QtCore.Signal = PyQt5.QtCore.pyqtSignal
    PyQt5.QtCore.Slot = PyQt5.QtCore.pyqtSlot
    PyQt5.QtCore.Property = PyQt5.QtCore.pyqtProperty

    # Add
    PyQt5.__wrapper_version__ = __version__
    PyQt5.__binding__ = "PyQt5"
    PyQt5.__binding_version__ = PyQt5.QtCore.PYQT_VERSION_STR
    PyQt5.__qt_version__ = PyQt5.QtCore.QT_VERSION_STR
    PyQt5.load_ui = pyqt_load_ui_wrap(version=5)

    return PyQt5


def _pyqt4():
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

    # Remap
    PyQt4.QtWidgets = PyQt4.QtGui
    PyQt4.QtCore.Signal = PyQt4.QtCore.pyqtSignal
    PyQt4.QtCore.Slot = PyQt4.QtCore.pyqtSlot
    PyQt4.QtCore.Property = PyQt4.QtCore.pyqtProperty
    PyQt4.QtCore.QItemSelection = PyQt4.QtGui.QItemSelection
    PyQt4.QtCore.QItemSelectionModel = PyQt4.QtGui.QItemSelectionModel

    # Add
    PyQt4.__wrapper_version__ = __version__
    PyQt4.__binding__ = "PyQt4"
    PyQt4.__binding_version__ = PyQt4.QtCore.PYQT_VERSION_STR
    PyQt4.__qt_version__ = PyQt4.QtCore.QT_VERSION_STR
    PyQt4.load_ui = pyqt_load_ui_wrap(version=4)

    return PyQt4


def _pyside2():
    import PySide2
    from PySide2 import QtGui, QtCore

    # Remap
    QtCore.QStringListModel = QtGui.QStringListModel

    # Add
    PySide2.__wrapper_version__ = __version__
    PySide2.__binding__ = "PySide2"
    PySide2.__binding_version__ = PySide2.__version__
    PySide2.__qt_version__ = PySide2.QtCore.qVersion()
    PySide2.load_ui = pyside_load_ui_wrap(version=2)

    return PySide2


def _pyside():
    import PySide
    from PySide import QtGui, QtCore

    # Remap
    PySide.QtWidgets = QtGui
    QtCore.QSortFilterProxyModel = QtGui.QSortFilterProxyModel
    QtCore.QStringListModel = QtGui.QStringListModel
    PySide.QtCore.QItemSelection = PySide.QtGui.QItemSelection
    PySide.QtCore.QItemSelectionModel = PySide.QtGui.QItemSelectionModel

    # Add
    PySide.__wrapper_version__ = __version__
    PySide.__binding__ = "PySide"
    PySide.__binding_version__ = PySide.__version__
    PySide.__qt_version__ = PySide.QtCore.qVersion()
    PySide.load_ui = pyside_load_ui_wrap(version=1)

    return PySide


def pyside_load_ui_wrap(version):
    if version == 1:
        from PySide import QtUiTools, QtCore
    elif version == 2:
        from PySide2 import QtUiTools, QtCore

    class UiLoader(QtUiTools.QUiLoader):
        def __init__(self, base_instance, custom_widgets=None):
            QtUiTools.QUiLoader.__init__(self, base_instance)
            self.base_instance = base_instance
            self.custom_widgets = custom_widgets

        def createWidget(self, class_name, parent=None, name=''):
            if parent is None and self.base_instance:
                return self.base_instance
            else:
                if class_name in self.availableWidgets():
                    widget = QtUiTools.QUiLoader.createWidget(self,
                                                              class_name,
                                                              parent, name)
                else:
                    try:
                        widget = self.custom_widgets[class_name](parent)
                    except (TypeError, KeyError):
                        raise Exception('No custom widget ' +
                                        class_name +
                                        ' found in custom_widgets' +
                                        ' param of UiLoader __init__.')
                if self.base_instance:
                    setattr(self.base_instance, name, widget)
                return widget

    def pyside_load_ui(fname, base_instance=None, custom_widgets=None):
        """Read Qt Designer .ui `fname`

        Args:
            fname (str): Absolute path to .ui file
            base_instance (widget, optional): Instance of the Qt base class.
            custom_widgets (widget): ?

        Usage:
            from Qt import load_ui
            class MyWindow(QtWidgets.QWidget):
                def __init__(self, parent=None):
                    fname = 'my_ui.ui'
                    load_ui(fname, self)
            window = MyWindow()

        Note:
            This function is based on the gist:
            https://gist.github.com/cpbotha/1b42a20c8f3eb9bb7cb8

        """

        def loadUi(fname, base_instance=None, custom_widgets=None):
            loader = UiLoader(base_instance, custom_widgets)
            widget = loader.load(fname)
            QtCore.QMetaObject.connectSlotsByName(widget)
            return widget

        return loadUi(fname, base_instance=base_instance,
                      custom_widgets=custom_widgets)

    return pyside_load_ui


def pyqt_load_ui_wrap(version):
    if version == 4:
        from PyQt4 import uic
    elif version == 5:
        from PyQt5 import uic

    def pyqt_load_ui(fname, base_instance=None, custom_widgets=None):
        """Read Qt Designer .ui `fname`

        Args:
            fname (str): Absolute path to .ui file
            base_instance (widget, optional): Instance of the Qt base class.
            custom_widgets (widget): ?

        Usage:
            from Qt import load_ui
            class MyWindow(QtWidgets.QWidget):
                def __init__(self, parent=None):
                    fname = 'my_ui.ui'
                    load_ui(fname, self)
            window = MyWindow()

        """

        if isinstance(base_instance, type(None)) and \
                isinstance(custom_widgets, type(None)):
            return uic.loadUi(fname)
        elif not isinstance(base_instance, type(None)) and \
                isinstance(custom_widgets, type(None)):
            return uic.loadUi(fname, base_instance)
        else:
            return uic.loadUi(fname, base_instance, custom_widgets)

    return pyqt_load_ui


def _log(text, verbose):
    if verbose:
        sys.stdout.write(text)


def _init():
    """Try loading each binding in turn

    Please note: the entire Qt module is replaced with this code:
        sys.modules["Qt"] = binding()

    This means no functions or variables can be called after
    this has executed.

    """

    preferred = os.getenv("QT_PREFERRED_BINDING")
    verbose = os.getenv("QT_VERBOSE") is not None
    bindings = (_pyside2, _pyqt5, _pyside, _pyqt4)

    if preferred:

        # Internal flag (used in installer)
        if preferred == "None":
            sys.modules[__name__].__wrapper_version__ = __version__
            return

        preferred = preferred.split(os.pathsep)
        available = {
            "PySide2": _pyside2,
            "PyQt5": _pyqt5,
            "PySide": _pyside,
            "PyQt4": _pyqt4
        }

        try:
            bindings = [available[binding] for binding in preferred]
        except KeyError:
            raise ImportError(
                "Available preferred Qt bindings: "
                "\n".join(preferred)
            )

    for binding in bindings:
        _log("Trying %s" % binding.__name__[1:], verbose)

        try:
            sys.modules[__name__] = binding()
            return

        except ImportError as e:
            _log(" - ImportError(\"%s\")\n" % e, verbose)

            continue

    # If not binding were found, throw this error
    raise ImportError("No Qt binding were found.")


_init()
