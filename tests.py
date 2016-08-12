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

    self.ui_qmainwindow = os.path.join(self.tempdir, "qmainwindow.ui")
    source_qmainwindow = u"""\
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>216</width>
    <height>149</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QGridLayout" name="gridLayout">
    <item row="0" column="0">
     <widget class="QLineEdit" name="lineEdit"/>
    </item>
   </layout>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>216</width>
     <height>22</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>

"""
    with io.open(self.ui_qmainwindow, "w", encoding="utf-8") as f:
        f.write(source_qmainwindow)

    self.ui_qwidget = os.path.join(self.tempdir, "qwidget.ui")
    source_qwidget = u"""\
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
    with io.open(self.ui_qwidget, "w", encoding="utf-8") as f:
        f.write(source_qwidget)

    self.ui_qdialog = os.path.join(self.tempdir, "qdialog.ui")
    source_qdialog = u"""\
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Dialog</class>
 <widget class="QDialog" name="Dialog">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>201</width>
    <height>176</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Dialog</string>
  </property>
  <layout class="QGridLayout" name="gridLayout">
   <item row="0" column="0">
    <widget class="QLineEdit" name="lineEdit"/>
   </item>
   <item row="1" column="0">
    <widget class="QDialogButtonBox" name="buttonBox">
     <property name="orientation">
      <enum>Qt::Horizontal</enum>
     </property>
     <property name="standardButtons">
      <set>QDialogButtonBox::Cancel|QDialogButtonBox::Ok</set>
     </property>
    </widget>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections>
  <connection>
   <sender>buttonBox</sender>
   <signal>accepted()</signal>
   <receiver>Dialog</receiver>
   <slot>accept()</slot>
   <hints>
    <hint type="sourcelabel">
     <x>248</x>
     <y>254</y>
    </hint>
    <hint type="destinationlabel">
     <x>157</x>
     <y>274</y>
    </hint>
   </hints>
  </connection>
  <connection>
   <sender>buttonBox</sender>
   <signal>rejected()</signal>
   <receiver>Dialog</receiver>
   <slot>reject()</slot>
   <hints>
    <hint type="sourcelabel">
     <x>316</x>
     <y>260</y>
    </hint>
    <hint type="destinationlabel">
     <x>286</x>
     <y>274</y>
    </hint>
   </hints>
  </connection>
 </connections>
</ui>

"""
    with io.open(self.ui_qdialog, "w", encoding="utf-8") as f:
        f.write(source_qdialog)

    self.ui_custom_pyqt = os.path.join(self.tempdir, "custom_widget.ui")
    source_custom_pyqt = u"""\
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="MyCustomWidget" name="customWidget">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>10</y>
      <width>113</width>
      <height>32</height>
     </rect>
    </property>
    <property name="text">
     <string>PushButton</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>125</width>
     <height>22</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <customwidgets>
  <customwidget>
   <class>MyCustomWidget</class>
   <extends>QPushButton</extends>
   <header>MyCustomClasses</header>
  </customwidget>
 </customwidgets>
 <resources/>
 <connections/>
</ui>

"""
    with io.open(self.ui_custom_pyqt, "w", encoding="utf-8") as f:
        f.write(source_custom_pyqt)


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


def test_load_ui_into_self_qmainwindow_pyside():
    """load_ui: Load widgets into self (QMainWindow) using PySide"""

    with pyside():
        from Qt import QtWidgets, load_ui

        class MainWindow(QtWidgets.QMainWindow):
            def __init__(self, parent=None):
                QtWidgets.QMainWindow.__init__(self, parent)
                load_ui(sys.modules[__name__].ui_qmainwindow, self)

        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()

        # Inherited from .ui file
        assert hasattr(window, "lineEdit")
        assert isinstance(window.__class__, type(QtWidgets.QMainWindow))
        assert isinstance(window.parent(), type(None))
        assert isinstance(window.lineEdit.__class__, type(QtWidgets.QWidget))
        assert window.lineEdit.text() == ''
        window.lineEdit.setText('Hello')
        assert window.lineEdit.text() == 'Hello'

        app.exit()


def test_load_ui_into_self_qwidget_pyside():
    """load_ui: Load widgets into self (QWidget) using PySide"""

    with pyside():
        from Qt import QtWidgets, load_ui

        class MainWindow(QtWidgets.QWidget):
            def __init__(self, parent=None):
                QtWidgets.QWidget.__init__(self, parent)
                load_ui(sys.modules[__name__].ui_qwidget, self)

        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()

        # Inherited from .ui file
        assert hasattr(window, "lineEdit")
        assert isinstance(window.__class__, type(QtWidgets.QWidget))
        assert isinstance(window.parent(), type(None))
        assert isinstance(window.lineEdit.__class__, type(QtWidgets.QWidget))
        assert window.lineEdit.text() == ''
        window.lineEdit.setText('Hello')
        assert window.lineEdit.text() == 'Hello'

        app.exit()


def test_load_ui_into_self_qdialog_pyside():
    """load_ui: Load widgets into self (QDialog) using PySide"""

    with pyside():
        from Qt import QtWidgets, load_ui

        class MainWindow(QtWidgets.QDialog):
            def __init__(self, parent=None):
                QtWidgets.QDialog.__init__(self, parent)
                load_ui(sys.modules[__name__].ui_qdialog, self)

        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()

        # Inherited from .ui file
        assert hasattr(window, "lineEdit")
        assert isinstance(window.__class__, type(QtWidgets.QDialog))
        assert isinstance(window.parent(), type(None))
        assert isinstance(window.lineEdit.__class__, type(QtWidgets.QWidget))
        assert window.lineEdit.text() == ''
        window.lineEdit.setText('Hello')
        assert window.lineEdit.text() == 'Hello'

        app.exit()


def test_load_ui_into_self_qmainwindow_pyqt4():
    """load_ui: Load widgets into self (QMainWindow) using PyQt4"""

    with pyqt4():
        from Qt import QtWidgets, load_ui

        class MainWindow(QtWidgets.QMainWindow):
            def __init__(self, parent=None):
                QtWidgets.QMainWindow.__init__(self, parent)
                load_ui(sys.modules[__name__].ui_qmainwindow, self)

        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()

        # From .ui file
        assert hasattr(window, "lineEdit")
        assert isinstance(window.__class__, type(QtWidgets.QMainWindow))
        assert isinstance(window.parent(), type(None))
        assert isinstance(window.lineEdit.__class__, type(QtWidgets.QWidget))
        assert window.lineEdit.text() == ''
        window.lineEdit.setText('Hello')
        assert window.lineEdit.text() == 'Hello'

        app.exit()


def test_load_ui_into_self_qwidget_pyqt4():
    """load_ui: Load widgets into self (QWidget) using PyQt4"""

    with pyqt4():
        from Qt import QtWidgets, load_ui

        class MainWindow(QtWidgets.QWidget):
            def __init__(self, parent=None):
                QtWidgets.QWidget.__init__(self, parent)
                load_ui(sys.modules[__name__].ui_qwidget, self)

        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()

        # From .ui file
        assert hasattr(window, "lineEdit")
        assert isinstance(window.__class__, type(QtWidgets.QWidget))
        assert isinstance(window.parent(), type(None))
        assert isinstance(window.lineEdit.__class__, type(QtWidgets.QWidget))
        assert window.lineEdit.text() == ''
        window.lineEdit.setText('Hello')
        assert window.lineEdit.text() == 'Hello'

        app.exit()


def test_load_ui_into_self_qdialog_pyqt4():
    """load_ui: Load widgets into self (QWidget) using PyQt4"""

    with pyqt4():
        from Qt import QtWidgets, load_ui

        class MainWindow(QtWidgets.QDialog):
            def __init__(self, parent=None):
                QtWidgets.QDialog.__init__(self, parent)
                load_ui(sys.modules[__name__].ui_qdialog, self)

        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()

        # From .ui file
        assert hasattr(window, "lineEdit")
        assert isinstance(window.__class__, type(QtWidgets.QDialog))
        assert isinstance(window.parent(), type(None))
        assert isinstance(window.lineEdit.__class__, type(QtWidgets.QWidget))
        assert window.lineEdit.text() == ''
        window.lineEdit.setText('Hello')
        assert window.lineEdit.text() == 'Hello'

        app.exit()


def test_load_ui_into_custom_pyside():
    """load_ui: Load widgets into widget (QMainWindow) using PySide"""

    with pyside():
        from Qt import QtWidgets, load_ui

        app = QtWidgets.QApplication(sys.argv)
        widget = load_ui(sys.modules[__name__].ui_qmainwindow)

        # From .ui file
        assert hasattr(widget, "lineEdit")
        assert isinstance(widget.__class__, type(QtWidgets.QMainWindow))
        assert isinstance(widget.parent(), type(None))
        assert isinstance(widget.lineEdit.__class__, type(QtWidgets.QWidget))
        assert widget.lineEdit.text() == ''
        widget.lineEdit.setText('Hello')
        assert widget.lineEdit.text() == 'Hello'

        app.exit()


def test_load_ui_into_custom_pyqt4():
    """load_ui: Load widgets into widget (QMainWindow) using PyQt4"""

    with pyqt4():
        from Qt import QtWidgets, load_ui

        app = QtWidgets.QApplication(sys.argv)
        widget = load_ui(sys.modules[__name__].ui_qmainwindow)

        # From .ui file
        assert hasattr(widget, "lineEdit")
        assert isinstance(widget.__class__, type(QtWidgets.QMainWindow))
        assert isinstance(widget.parent(), type(None))
        assert isinstance(widget.lineEdit.__class__, type(QtWidgets.QWidget))
        assert widget.lineEdit.text() == ''
        widget.lineEdit.setText('Hello')
        assert widget.lineEdit.text() == 'Hello'

        app.exit()


def test_load_ui_connection_pyside():
    """load_ui: Signals in PySide"""

    with pyside():
        import sys
        from Qt import QtWidgets, load_ui

        def setup_ui(base_instance=None):
            return load_ui(sys.modules[__name__].ui_qmainwindow, base_instance)

        app = QtWidgets.QApplication(sys.argv)
        Ui = type(setup_ui())  # Get the un-instantiated class

        class MyWidget(Ui):          # Inherit from it.
            def __init__(self, parent=None):
                super(MyWidget, self).__init__(parent)
                setup_ui(self)
                self.x = False
                self.lineEdit.textChanged.connect(self.some_method)
                self.lineEdit.setText('hello')
                assert self.x is True

            def some_method(self):
                self.x = True

        my_widget = MyWidget()
        my_widget.show()


def test_load_ui_connection_pyqt4():
    """load_ui: Signals in PyQt4"""

    with pyqt4():
        import sys
        from Qt import QtWidgets, load_ui

        def setup_ui(base_instance=None):
            return load_ui(sys.modules[__name__].ui_qmainwindow, base_instance)

        app = QtWidgets.QApplication(sys.argv)
        Ui = type(setup_ui())  # Get the un-instantiated class

        class MyWidget(Ui):          # Inherit from it.
            def __init__(self, parent=None):
                super(MyWidget, self).__init__(parent)
                setup_ui(self)
                self.x = False
                self.lineEdit.textChanged.connect(self.some_method)
                self.lineEdit.setText('hello')
                assert self.x is True

            def some_method(self):
                self.x = True

        my_widget = MyWidget()
        my_widget.show()


if PYTHON == 2:
    def test_sip_api_already_set():
        """Raise ImportError if sip API v1 was already set (Python 2.x only)"""

        with pyqt4():
            __import__("PyQt4.QtCore")  # Bypass linter warning
            import sip
            sip.setapi("QString", 1)
            assert_raises(ImportError, __import__, "Qt")
