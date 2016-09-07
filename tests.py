"""Tests that run once"""

import io
import os
import sys
import imp
import shutil
import tempfile
import subprocess

from nose.tools import (
    assert_raises,
)

PYTHON = sys.version_info[0]  # e.g. 2 or 3


self = sys.modules[__name__]


def setup():
    """Module-wide initialisation

    This function runs once, followed by teardown() below once
    all tests have completed.

    """

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
""")


def teardown():
    shutil.rmtree(self.tempdir)


def binding(binding):
    """Isolate test to a particular binding

    When used, tests inside the if-statement are run independently
    with the given binding.

    Without this function, a test is run once for each binding.

    """

    return os.getenv("QT_PREFERRED_BINDING") == binding


def test_environment():
    """Tests require all bindings to be installed"""

    imp.find_module("PySide")
    imp.find_module("PySide2")
    imp.find_module("PyQt4")
    imp.find_module("PyQt5")


def test_load_ui_returntype():
    """load_ui returns an instance of QObject"""

    import sys
    from Qt import QtWidgets, QtCore, load_ui
    app = QtWidgets.QApplication(sys.argv)
    obj = load_ui(self.ui_qwidget)
    assert isinstance(obj, QtCore.QObject)
    app.exit()


def test_preferred_none():
    """Preferring None shouldn't import anything"""

    os.environ["QT_PREFERRED_BINDING"] = "None"
    import Qt
    assert Qt.__name__ == "Qt", Qt


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


def test_convert_simple():
    """python -m Qt --convert works in general"""
    before = """\
from PySide2 import QtCore, QtGui, QtWidgets

class Ui_uic(object):
    def setupUi(self, uic):
        self.retranslateUi(uic)

    def retranslateUi(self, uic):
        self.pushButton_2.setText(
            QtWidgets.QApplication.translate("uic", "NOT Ok", None, -1))
"""

    after = """\
from Qt import QtCore, QtGui, QtWidgets

class Ui_uic(object):
    def setupUi(self, uic):
        self.retranslateUi(uic)

    def retranslateUi(self, uic):
        self.pushButton_2.setText(
            Qt.translate("uic", "NOT Ok", None, -1))
"""

    import Qt
    assert Qt.convert(before) == after, after


if binding("PyQt4"):
    def test_preferred_pyqt4():
        """QT_PREFERRED_BINDING = PyQt4 properly forces the binding"""
        import Qt
        assert Qt.__name__ == "PyQt4", ("PyQt4 should have been picked, "
                                        "instead got %s" % Qt)

    def test_sip_api_qtpy():
        """Preferred binding PyQt4 should have sip version 2"""

        __import__("Qt")  # Bypass linter warning
        import sip
        assert sip.getapi("QString") == 2, ("PyQt4 API version should be 2, "
                                            "instead is %s"
                                            % sip.getapi("QString"))

    if PYTHON == 2:
        def test_sip_api_already_set():
            """Raise ImportError if sip API v1 was already set"""

            __import__("PyQt4.QtCore")  # Bypass linter warning
            import sip
            sip.setapi("QString", 1)
            assert_raises(ImportError, __import__, "Qt")


if binding("PyQt5"):
    def test_preferred_pyqt5():
        """QT_PREFERRED_BINDING = PyQt5 properly forces the binding"""
        import Qt
        assert Qt.__name__ == "PyQt5", ("PyQt5 should have been picked, "
                                        "instead got %s" % Qt)


if binding("PySide"):
    def test_preferred_pyside():
        """QT_PREFERRED_BINDING = PySide properly forces the binding"""
        import Qt
        assert Qt.__name__ == "PySide", ("PySide should have been picked, "
                                         "instead got %s" % Qt)


if binding("PySide2"):
    def test_preferred_pyside2():
        """QT_PREFERRED_BINDING = PySide2 properly forces the binding"""
        import Qt
        assert Qt.__name__ == "PySide2", ("PySide2 should have been picked, "
                                          "instead got %s" % Qt)

    def test_coexistence():
        """Qt.py may be use alongside the actual binding"""

        from Qt import QtCore
        import PySide.QtGui

        # Qt remaps QStringListModel
        assert QtCore.QStringListModel

        # But does not delete the original
        assert PySide.QtGui.QStringListModel


if binding("PySide") or binding("PySide2"):
    def test_multiple_preferred():
        """QT_PREFERRED_BINDING = more than one binding excludes others"""

        # PySide is the more desirable binding
        os.environ["QT_PREFERRED_BINDING"] = os.pathsep.join(
            ["PySide", "PySide2"])

        import Qt
        assert Qt.__name__ == "PySide", ("PySide should have been picked, "
                                         "instead got %s" % Qt)
