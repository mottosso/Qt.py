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
    >> import sys
    >> from Qt import QtWidgets
    >> app = QtWidgets.QApplication(sys.argv)
    >> button = QtWidgets.QPushButton("Hello World")
    >> button.show()
    >> app.exec_()

"""

import os
import sys
import shutil

self = sys.modules[__name__]

self.__version__ = "0.6.1"

self.__added__ = list()     # All unique members of Qt.py
self.__remapped__ = list()  # Members copied from elsewhere
self.__modified__ = list()  # Existing members modified in some way

# Below members are set dynamically on import relative the original binding.
self.__qt_version__ = "0.0.0"
self.__binding__ = "None"
self.__binding_version__ = "0.0.0"
self.load_ui = lambda fname: None
self.translate = lambda context, sourceText, disambiguation, n: None
self.setSectionResizeMode = lambda *args, **kwargs: None


def convert(lines):
    """Convert compiled .ui file from PySide2 to Qt.py

    Arguments:
        lines (list): Each line of of .ui file

    Usage:
        >> with open("myui.py") as f:
        ..   lines = convert(f.readlines())

    """

    def parse(line):
        line = line.replace("from PySide2 import", "from Qt import")
        line = line.replace("QtWidgets.QApplication.translate",
                            "Qt.QtCompat.translate")
        return line

    parsed = list()
    for line in lines:
        line = parse(line)
        parsed.append(line)

    return parsed


def _remap(object, name, value, safe=True):
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
        self.__modified__.append(name)

    self.__remapped__.append(name)

    setattr(object, name, value)


def _add(object, name, value):
    """Append to self, accessible via Qt.QtCompat"""
    self.__added__.append(name)
    setattr(self, name, value)


def _pyqt5():
    import PyQt5.Qt
    from PyQt5 import QtCore, QtWidgets, uic

    _remap(QtCore, "Signal", QtCore.pyqtSignal)
    _remap(QtCore, "Slot", QtCore.pyqtSlot)
    _remap(QtCore, "Property", QtCore.pyqtProperty)

    _add(PyQt5, "__binding__", PyQt5.__name__)
    _add(PyQt5, "load_ui", lambda fname: uic.loadUi(fname))
    _add(PyQt5, "translate", lambda context, sourceText, disambiguation, n: (
        QtCore.QCoreApplication(context, sourceText,
                                disambiguation, n)))
    _add(PyQt5,
         "setSectionResizeMode",
         QtWidgets.QHeaderView.setSectionResizeMode)

    _maintain_backwards_compatibility(PyQt5)

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
    from PyQt4 import QtCore, QtGui, uic

    _remap(PyQt4, "QtWidgets", QtGui)
    _remap(QtCore, "Signal", QtCore.pyqtSignal)
    _remap(QtCore, "Slot", QtCore.pyqtSlot)
    _remap(QtCore, "Property", QtCore.pyqtProperty)
    _remap(QtCore, "QItemSelection", QtGui.QItemSelection)
    _remap(QtCore, "QStringListModel", QtGui.QStringListModel)
    _remap(QtCore, "QItemSelectionModel", QtGui.QItemSelectionModel)
    _remap(QtCore, "QSortFilterProxyModel", QtGui.QSortFilterProxyModel)
    _remap(QtCore, "QAbstractProxyModel", QtGui.QAbstractProxyModel)

    try:
        from PyQt4 import QtWebKit
        _remap(PyQt4, "QtWebKitWidgets", QtWebKit)
    except ImportError:
        # QtWebkit is optional in Qt , therefore might not be available
        pass

    _add(PyQt4, "QtCompat", self)
    _add(PyQt4, "__binding__", PyQt4.__name__)
    _add(PyQt4, "load_ui", lambda fname: uic.loadUi(fname))
    _add(PyQt4, "translate", lambda context, sourceText, disambiguation, n: (
        QtCore.QCoreApplication(context, sourceText,
                                disambiguation, None, n)))
    _add(PyQt4, "setSectionResizeMode", QtGui.QHeaderView.setResizeMode)

    _maintain_backwards_compatibility(PyQt4)

    return PyQt4


def _pyside2():
    import PySide2
    from PySide2 import QtGui, QtWidgets, QtCore, QtUiTools

    _remap(QtCore, "QStringListModel", QtGui.QStringListModel)

    _add(PySide2, "__binding__", PySide2.__name__)
    _add(PySide2, "load_ui", lambda fname: QtUiTools.QUiLoader().load(fname))
    _add(PySide2, "translate", lambda context, sourceText, disambiguation, n: (
        QtCore.QCoreApplication(context, sourceText,
                                disambiguation, None, n)))
    _add(PySide2,
         "setSectionResizeMode",
         QtWidgets.QHeaderView.setSectionResizeMode)

    _maintain_backwards_compatibility(PySide2)

    return PySide2


def _pyside():
    import PySide
    from PySide import QtGui, QtCore, QtUiTools

    _remap(PySide, "QtWidgets", QtGui)
    _remap(QtCore, "QSortFilterProxyModel", QtGui.QSortFilterProxyModel)
    _remap(QtCore, "QStringListModel", QtGui.QStringListModel)
    _remap(QtCore, "QItemSelection", QtGui.QItemSelection)
    _remap(QtCore, "QItemSelectionModel", QtGui.QItemSelectionModel)
    _remap(QtCore, "QAbstractProxyModel", QtGui.QAbstractProxyModel)

    try:
        from PySide import QtWebKit
        _remap(PySide, "QtWebKitWidgets", QtWebKit)
    except ImportError:
        # QtWebkit is optional in Qt, therefore might not be available
        pass

    _add(PySide, "__binding__", PySide.__name__)
    _add(PySide, "load_ui", lambda fname: QtUiTools.QUiLoader().load(fname))
    _add(PySide, "translate", lambda context, sourceText, disambiguation, n: (
        QtCore.QCoreApplication(context, sourceText,
                                disambiguation, None, n)))
    _add(PySide, "setSectionResizeMode", QtGui.QHeaderView.setResizeMode)

    _maintain_backwards_compatibility(PySide)

    return PySide


def _log(text, verbose):
    if verbose:
        sys.stdout.write(text + "\n")


def cli(args):
    """Qt.py command-line interface"""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--convert",
                        help="Path to compiled Python module, e.g. my_ui.py")
    parser.add_argument("--compile",
                        help="Accept raw .ui file and compile with native "
                             "PySide2 compiler.")
    parser.add_argument("--stdout",
                        help="Write to stdout instead of file",
                        action="store_true")
    parser.add_argument("--stdin",
                        help="Read from stdin instead of file",
                        action="store_true")

    args = parser.parse_args(args)

    if args.stdout:
        raise NotImplementedError("--stdout")

    if args.stdin:
        raise NotImplementedError("--stdin")

    if args.compile:
        raise NotImplementedError("--compile")

    if args.convert:
        sys.stdout.write("#\n"
                         "# WARNING: --convert is an ALPHA feature.\n#\n"
                         "# See https://github.com/mottosso/Qt.py/pull/132\n"
                         "# for details.\n"
                         "#\n")

        #
        # ------> Read
        #
        with open(args.convert) as f:
            lines = convert(f.readlines())

        backup = "%s_backup%s" % os.path.splitext(args.convert)
        sys.stdout.write("Creating \"%s\"..\n" % backup)
        shutil.copy(args.convert, backup)

        #
        # <------ Write
        #
        with open(args.convert, "w") as f:
            f.write("".join(lines))

        sys.stdout.write("Successfully converted \"%s\"\n" % args.convert)


def init():
    """Try loading each binding in turn

    Please note: the entire Qt module is replaced with this code:
        sys.modules["Qt"] = binding()

    This means no functions or variables can be called after
    this has executed.

    For debugging and testing, this module may be accessed
    through `Qt.__shim__`.

    """

    preferred = os.getenv("QT_PREFERRED_BINDING")
    verbose = os.getenv("QT_VERBOSE") is not None
    bindings = (_pyside2, _pyqt5, _pyside, _pyqt4)

    if preferred:
        # Internal flag (used in installer)
        if preferred == "None":
            self.__wrapper_version__ = self.__version__
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
        _log("Trying %s" % binding.__name__, verbose)

        try:
            binding = binding()

        except ImportError as e:
            _log(" - ImportError(\"%s\")" % e, verbose)
            continue

        else:
            # Reference to this module
            binding.__shim__ = self
            binding.QtCompat = self

            sys.modules.update({
                __name__: binding,

                # Fix #133, `from Qt.QtWidgets import QPushButton`
                __name__ + ".QtWidgets": binding.QtWidgets

            })

            return

    # If not binding were found, throw this error
    raise ImportError("No Qt binding were found.")


def _maintain_backwards_compatibility(binding):
    """Add members found in prior versions up till the next major release

    These members are to be considered deprecated. When a new major
    release is made, these members are removed.

    """

    for member in ("__binding__",
                   "__binding_version__",
                   "__qt_version__",
                   "__added__",
                   "__remapped__",
                   "__modified__",
                   "convert",
                   "load_ui",
                   "translate"):
        setattr(binding, member, getattr(self, member))
        self.__added__.append(member)

    setattr(binding, "__wrapper_version__", self.__version__)
    self.__added__.append("__wrapper_version__")


cli(sys.argv[1:]) if __name__ == "__main__" else init()
