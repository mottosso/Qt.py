"""Nose tests

Usage:
    $ nosetests .

"""

import os
import io
import sys
import imp
import shutil
import tempfile
import subprocess
import contextlib

from nose.tools import (
    assert_raises,
)

PYTHON = sys.version_info[0]  # e.g. 2 or 3

self = sys.modules[__name__]


def setup():
    self.tempdir = tempfile.mkdtemp()
    self.ui_qwidget = os.path.join(self.tempdir, "qwidget.ui")

    with io.open(self.ui_qwidget, "w", encoding="utf-8") as f:
        f.write(u"""\
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>235</width>
    <height>149</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <layout class="QGridLayout" name="gridLayout">
   <item row="0" column="0">
    <widget class="QLineEdit" name="lineEdit"/>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections/>
</ui>
"""
)


def teardown():
    shutil.rmtree(self.tempdir)


@contextlib.contextmanager
def pyqt4():
    os.environ["QT_PREFERRED_BINDING"] = "PyQt4"
    yield
    os.environ.pop("QT_PREFERRED_BINDING")


@contextlib.contextmanager
def pyqt5():
    os.environ["QT_PREFERRED_BINDING"] = "PyQt5"
    yield
    os.environ.pop("QT_PREFERRED_BINDING")


@contextlib.contextmanager
def pyside():
    os.environ["QT_PREFERRED_BINDING"] = "PySide"
    yield
    os.environ.pop("QT_PREFERRED_BINDING")


@contextlib.contextmanager
def pyside2():
    os.environ["QT_PREFERRED_BINDING"] = "PySide2"
    yield
    os.environ.pop("QT_PREFERRED_BINDING")


def test_environment():
    """Tests require all bindings to be installed"""

    imp.find_module("PySide")
    imp.find_module("PySide2")
    imp.find_module("PyQt4")
    imp.find_module("PyQt5")


def test_preferred_pyqt4():
    """Setting QT_PREFERRED_BINDING to PyQt4 properly forces the binding"""
    with pyqt4():
        import Qt
        assert Qt.__name__ == "PyQt4", ("PyQt4 should have been picked, "
                                        "instead got %s" % Qt)


def test_preferred_pyqt5():
    """Setting QT_PREFERRED_BINDING to PyQt5 properly forces the binding"""
    with pyqt5():
        import Qt
        assert Qt.__name__ == "PyQt5", ("PyQt5 should have been picked, "
                                        "instead got %s" % Qt)


def test_preferred_pyside():
    """Setting QT_PREFERRED_BINDING to PySide properly forces the binding"""
    with pyside():
        import Qt
        assert Qt.__name__ == "PySide", ("PySide should have been picked, "
                                         "instead got %s" % Qt)


def test_preferred_pyside2():
    """Setting QT_PREFERRED_BINDING to PySide2 properly forces the binding"""
    with pyside2():
        import Qt
        assert Qt.__name__ == "PySide2", ("PySide2 should have been picked, "
                                          "instead got %s" % Qt)


def test_multiple_preferred():
    """Setting QT_PREFERRED_BINDING to more than one binding excludes others"""

    # PySide is the more desirable binding
    os.environ["QT_PREFERRED_BINDING"] = os.pathsep.join(["PySide", "PySide2"])

    import Qt
    assert Qt.__name__ == "PySide", ("PySide should have been picked, "
                                     "instead got %s" % Qt)


def test_preferred_none():
    """Preferring None shouldn't import anything"""

    os.environ["QT_PREFERRED_BINDING"] = "None"
    import Qt
    assert Qt.__name__ == "Qt", Qt


def test_coexistence():
    """Qt.py may be use alongside the actual binding"""

    with pyside():
        from Qt import QtCore
        import PySide.QtGui

        # Qt remaps QStringListModel
        assert QtCore.QStringListModel

        # But does not delete the original
        assert PySide.QtGui.QStringListModel


def test_sip_api_qtpy():
    """Preferred binding PyQt4 should have sip version 2"""

    with pyqt4():
        __import__("Qt")  # Bypass linter warning
        import sip
        assert sip.getapi("QString") == 2, ("PyQt4 API version should be 2, "
                                            "instead is %s"
                                            % sip.getapi("QString"))


def test_pyside_load_ui_returntype():
    """load_ui returns an instance of QObject with PySide"""
    
    with pyside():
        import sys
        from Qt import QtWidgets, QtCore, load_ui
        app = QtWidgets.QApplication(sys.argv)
        obj = load_ui(self.ui_qwidget)
        assert isinstance(obj, QtCore.QObject)


def test_pyqt4_load_ui_returntype():
    """load_ui returns an instance of QObject with PyQt4"""
    
    with pyqt4():
        import sys
        from Qt import QtWidgets, QtCore, load_ui
        app = QtWidgets.QApplication(sys.argv)
        obj = load_ui(self.ui_qwidget)
        assert isinstance(obj, QtCore.QObject)


def test_pyside2_load_ui_returntype():
    """load_ui returns an instance of QObject with PySide2"""
    
    with pyside2():
        import sys
        from Qt import QtWidgets, QtCore, load_ui
        app = QtWidgets.QApplication(sys.argv)
        obj = load_ui(self.ui_qwidget)
        assert isinstance(obj, QtCore.QObject)


def test_pyqt5_load_ui_returntype():
    """load_ui returns an instance of QObject with PyQt5"""
    
    with pyqt5():
        import sys
        from Qt import QtWidgets, QtCore, load_ui
        app = QtWidgets.QApplication(sys.argv)
        obj = load_ui(self.ui_qwidget)
        assert isinstance(obj, QtCore.QObject)


def test_vendoring():
    """Qt.py may be bundled along with another library/project

    Create toy project

    from project.vendor import Qt  # Absolute
    from .vendor import Qt         # Relative

    project/
        vendor/
            __init__.py
        __init__.py

    """

    project = os.path.join(self.tempdir, "myproject")
    vendor = os.path.join(project, "vendor")

    os.makedirs(vendor)

    # Make packages out of folders
    with open(os.path.join(project, "__init__.py"), "w") as f:
        f.write("from .vendor.Qt import QtWidgets")

    with open(os.path.join(vendor, "__init__.py"), "w") as f:
        f.write("\n")

    # Copy real Qt.py into myproject
    shutil.copy(os.path.join(os.path.dirname(__file__), "Qt.py"),
                os.path.join(vendor, "Qt.py"))

    print("Testing relative import..")
    assert subprocess.call(
        [sys.executable, "-c", "import myproject"],
        cwd=self.tempdir,
        stdout=subprocess.PIPE,    # With nose process isolation, buffer can
        stderr=subprocess.STDOUT,  # easily get full and throw an error.
    ) == 0

    print("Testing absolute import..")
    assert subprocess.call(
        [sys.executable, "-c", "from myproject.vendor.Qt import QtWidgets"],
        cwd=self.tempdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ) == 0

    print("Testing direct import..")
    assert subprocess.call(
        [sys.executable, "-c", "import myproject.vendor.Qt"],
        cwd=self.tempdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ) == 0


if PYTHON == 2:
    def test_sip_api_already_set():
        """Raise ImportError if sip API v1 was already set (Python 2.x only)"""

        with pyqt4():
            __import__("PyQt4.QtCore")  # Bypass linter warning
            import sip
            sip.setapi("QString", 1)
            assert_raises(ImportError, __import__, "Qt")
