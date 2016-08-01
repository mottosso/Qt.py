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
    self.ui = os.path.join(self.tempdir, "temp.ui")

    source = u"""\
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>400</width>
    <height>300</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <widget class="QPushButton" name="pushButton">
   <property name="geometry">
    <rect>
     <x>140</x>
     <y>120</y>
     <width>90</width>
     <height>27</height>
    </rect>
   </property>
   <property name="text">
    <string>PushButton</string>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>

"""

    with io.open(self.ui, "w", encoding="utf-8") as f:
        f.write(source)


def teardown():
    shutil.rmtree(self.tempdir)


@contextlib.contextmanager
def pyqt4():
    os.environ["QT_PREFERRED_BINDING"] = "PyQt4"
    yield
    os.environ.pop("QT_PREFERRED_BINDING")


@contextlib.contextmanager
def pyside():
    os.environ["QT_PREFERRED_BINDING"] = "PySide"
    yield
    os.environ.pop("QT_PREFERRED_BINDING")


def test_environment():
    """Tests require PySide and PyQt4 bindings to be installed"""

    imp.find_module("PySide")
    imp.find_module("PyQt4")

    # These should *not* be available
    assert_raises(ImportError, imp.find_module, "PySide2")
    assert_raises(ImportError, imp.find_module, "PyQt5")


def test_preferred():
    """Setting QT_PREFERRED_BINDING properly forces a particular binding"""
    import Qt

    # PySide is the more desirable binding
    assert Qt.__name__ != "PyQt4", ("PySide should have been picked, "
                                    "instead got %s" % Qt)

    # Try again
    sys.modules.pop("Qt")

    with pyside():
        import Qt
        assert Qt.__name__ == "PySide", ("PySide should have been picked, "
                                         "instead got %s" % Qt)


def test_multiple_preferred():
    """Setting QT_PREFERRED_BINDING to more than one binding excludes others

    PyQt5 is not available on this system, and PySide is preferred over PyQt4,
    however this tests should prove that it should still pick up PyQt4
    when preferred.

    """

    # However
    os.environ["QT_PREFERRED_BINDING"] = os.pathsep.join(["PyQt5", "PyQt4"])
    import Qt

    # PySide is the more desirable binding
    assert Qt.__name__ == "PyQt4", ("PyQt4 should have been picked, "
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
        ["python", "-c", "import myproject"],
        cwd=self.tempdir,
        stdout=subprocess.PIPE,    # With nose process isolation, buffer can
        stderr=subprocess.STDOUT,  # easily get full and throw an error.
    ) == 0

    print("Testing absolute import..")
    assert subprocess.call(
        ["python", "-c", "from myproject.vendor.Qt import QtWidgets"],
        cwd=self.tempdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ) == 0

    print("Testing direct import..")
    assert subprocess.call(
        ["python", "-c", "import myproject.vendor.Qt"],
        cwd=self.tempdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ) == 0


def test_load_ui_into_self_pyside():
    """load_ui: Load widgets into self using PySide"""

    with pyside():
        from Qt import QtWidgets, load_ui

        class MainWindow(QtWidgets.QMainWindow):
            def __init__(self, parent=None):
                QtWidgets.QMainWindow.__init__(self, parent)
                load_ui(sys.modules[__name__].ui, self)

        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()

        # Inherited from .ui file
        assert hasattr(window, "pushButton")
        app.exit()


def test_load_ui_into_self_pyqt4():
    """load_ui: Load widgets into self using PyQt4"""

    with pyqt4():
        from Qt import QtWidgets, load_ui

        class MainWindow(QtWidgets.QMainWindow):
            def __init__(self, parent=None):
                QtWidgets.QMainWindow.__init__(self, parent)
                load_ui(sys.modules[__name__].ui, self)

        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()

        # Inherited from .ui file
        assert hasattr(window, "pushButton")
        app.exit()


def test_load_ui_into_custom_pyside():
    """load_ui: Load widgets into custom using PySide"""

    with pyside():
        from Qt import QtWidgets, load_ui

        app = QtWidgets.QApplication(sys.argv)
        widget = load_ui(sys.modules[__name__].ui)

        # From .ui file
        assert hasattr(widget, "pushButton")
        app.exit()


def test_load_ui_into_custom_pyqt4():
    """load_ui: Load widgets into custom using PyQt4"""

    with pyqt4():
        from Qt import QtWidgets, load_ui

        app = QtWidgets.QApplication(sys.argv)
        widget = load_ui(sys.modules[__name__].ui)

        # From .ui file
        assert hasattr(widget, "pushButton")
        app.exit()


if PYTHON == 2:
    def test_sip_api_already_set():
        """Raise ImportError if sip API v1 was already set (Python 2.x only)"""

        with pyqt4():
            __import__("PyQt4.QtCore")  # Bypass linter warning
            import sip
            sip.setapi("QString", 1)
            assert_raises(ImportError, __import__, "Qt")
