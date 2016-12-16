"""The MIT License (MIT)

Copyright (c) 2016 Marcus Ottosson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

Map all bindings to PySide2

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

# Flags from environment variables
QT_VERBOSE = bool(os.getenv("QT_VERBOSE"))                # Extra output
QT_TESTING = bool(os.getenv("QT_TESTING"))                # Extra constraints
QT_PREFERRED_BINDING = os.getenv("QT_PREFERRED_BINDING")  # Override default

self = sys.modules[__name__]

# Internal members, may be used externally for debugging
self.__added__ = list()     # All members added to QtCompat
self.__remapped__ = list()  # Members copied from elsewhere
self.__modified__ = list()  # Existing members modified in some way

# Below members are set dynamically on import relative the original binding.
self.__version__ = "0.6.9"
self.__qt_version__ = "0.0.0"
self.__binding__ = "None"
self.__binding_version__ = "0.0.0"

self.load_ui = lambda fname: None
self.translate = lambda context, sourceText, disambiguation, n: None
self.setSectionResizeMode = lambda logicalIndex, hide: None

# All members of this module is directly accessible via QtCompat
# Take care not to access any "private" members; i.e. those with
# a leading underscore.
QtCompat = self


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

    if QT_TESTING and safe:
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
    setattr(object, name, value)


def _pyqt5():
    import PyQt5.Qt
    from PyQt5 import QtCore, QtWidgets, uic

    _remap(QtCore, "Signal", QtCore.pyqtSignal)
    _remap(QtCore, "Slot", QtCore.pyqtSlot)
    _remap(QtCore, "Property", QtCore.pyqtProperty)

    _add(QtCompat, "__binding__", PyQt5.__name__)
    _add(QtCompat, "__binding_version__", PyQt5.QtCore.PYQT_VERSION_STR)
    _add(QtCompat, "__qt_version__", PyQt5.QtCore.QT_VERSION_STR)
    _add(QtCompat, "load_ui", lambda fname: uic.loadUi(fname))
    _add(QtCompat, "translate", QtCore.QCoreApplication.translate)
    _add(QtCompat, "setSectionResizeMode",
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
        "QtWebkit is optional in Qt , therefore might not be available"

    _add(QtCompat, "__binding__", PyQt4.__name__)
    _add(QtCompat, "__binding_version__", PyQt4.QtCore.PYQT_VERSION_STR)
    _add(QtCompat, "__qt_version__", PyQt4.QtCore.QT_VERSION_STR)
    _add(QtCompat, "load_ui", lambda fname: uic.loadUi(fname))
    _add(QtCompat, "setSectionResizeMode", QtGui.QHeaderView.setResizeMode)

    # PySide2 differs from Qt4 in that Qt4 has one extra argument
    # which is always `None`. The lambda arguments represents the PySide2
    # interface, whereas the arguments passed to `.translate` represent
    # those expected of a Qt4 binding.
    _add(QtCompat, "translate",
         lambda context, sourceText, disambiguation, n:
         QtCore.QCoreApplication.translate(context,
                                           sourceText,
                                           disambiguation,
                                           QtCore.QCoreApplication.CodecForTr,
                                           n))

    _maintain_backwards_compatibility(PyQt4)

    return PyQt4


def _pyside2():
    import PySide2
    from PySide2 import QtGui, QtWidgets, QtCore, QtUiTools

    _remap(QtCore, "QStringListModel", QtGui.QStringListModel)

    _add(QtCompat, "__binding__", PySide2.__name__)
    _add(QtCompat, "__binding_version__", PySide2.__version__)
    _add(QtCompat, "__qt_version__", PySide2.QtCore.qVersion())
    _add(QtCompat, "load_ui", lambda fname: QtUiTools.QUiLoader().load(fname))

    _add(QtCompat, "setSectionResizeMode",
         QtWidgets.QHeaderView.setSectionResizeMode)

    _add(QtCompat, "translate", QtCore.QCoreApplication.translate)

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
        "QtWebkit is optional in Qt, therefore might not be available"

    _add(QtCompat, "__binding__", PySide.__name__)
    _add(QtCompat, "__binding_version__", PySide.__version__)
    _add(QtCompat, "__qt_version__", PySide.QtCore.qVersion())
    _add(QtCompat, "load_ui", lambda fname: QtUiTools.QUiLoader().load(fname))
    _add(QtCompat, "setSectionResizeMode", QtGui.QHeaderView.setResizeMode)

    _add(QtCompat, "translate",
         lambda context, sourceText, disambiguation, n:
         QtCore.QCoreApplication.translate(context,
                                           sourceText,
                                           disambiguation,
                                           QtCore.QCoreApplication.CodecForTr,
                                           n))

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

    bindings = (_pyside2, _pyqt5, _pyside, _pyqt4)

    if QT_PREFERRED_BINDING:
        # Internal flag (used in installer)
        if QT_PREFERRED_BINDING == "None":
            self.__wrapper_version__ = self.__version__
            return

        preferred = QT_PREFERRED_BINDING.split(os.pathsep)
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
        _log("Trying %s" % binding.__name__, QT_VERBOSE)

        try:
            binding = binding()

        except ImportError as e:
            _log(" - ImportError(\"%s\")" % e, QT_VERBOSE)
            continue

        else:
            # Reference to this module
            binding.QtCompat = self
            binding.__shim__ = self  # DEPRECATED

            sys.modules.update({
                __name__: binding,

                # Fix #133, `from Qt.QtWidgets import QPushButton`
                __name__ + ".QtWidgets": binding.QtWidgets,

                # Fix #158 `import Qt.QtCore;Qt.QtCore.Signal`
                __name__ + ".QtCore": binding.QtCore,
                __name__ + ".QtGui": binding.QtGui,

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
