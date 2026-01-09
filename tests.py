# coding=utf-8
"""Tests that run once"""

import io
import os
import re
import sys
import imp
import shutil
import tempfile
import textwrap
import subprocess
import contextlib
import json
from pathlib import Path

# Third-party dependency
import six


try:
    # Try importing assert_raises from nose.tools
    from nose.tools import assert_raises
except ImportError:
    # Fallback: Define assert_raises using unittest if the import fails
    import unittest

    def assert_raises(expected_exception, callable_obj=None, *args, **kwargs):
        """
        Custom implementation of assert_raises using unittest.

        Parameters:
        - expected_exception: The exception type that is expected to be raised.
        - callable_obj: The callable object that is expected to raise the exception.
        - *args, **kwargs: Arguments and keyword arguments to pass to the callable object.

        Usage example:
        with assert_raises(SomeException):
            function_that_raises_some_exception()
        """
        context = unittest.TestCase().assertRaises(expected_exception)

        # If callable_obj is provided, directly call the function with the context manager
        if callable_obj:
            with context:
                callable_obj(*args, **kwargs)
        else:
            # Otherwise, return the context manager to be used with a 'with' statement
            return context


REPO_ROOT = Path(__file__).parent


# NOTE: When building multi-line strings use this format to improve code folding.
# dedent is mostly needed when your check cares about the leading white space.
# variable = textwrap.dedent(
#     """\
#     Example text
#     with common leading white space removed
#         additional indents are preserved.
#     The \\ at the top is important as it ensures the first line is indented
#     the same as all other lines.
#     """
# )


@contextlib.contextmanager
def captured_output():
    new_out, new_err = six.StringIO(), six.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def CustomWidget(parent=None):
    """
    Wrap CustomWidget class into a function to avoid global Qt import
    """
    from Qt import QtWidgets

    class Widget(QtWidgets.QWidget):
        pass

    return Widget(parent)


self = sys.modules[__name__]


qwidget_ui = textwrap.dedent(
    """\
    <?xml version="1.0" encoding="UTF-8"?>
    <ui version="4.0">
     <class>Form</class>
     <widget class="QWidget" name="Form">
      <property name="geometry">
       <rect>
        <x>0</x>
        <y>0</y>
        <width>507</width>
        <height>394</height>
       </rect>
      </property>
      <property name="windowTitle">
       <string>Form</string>
      </property>
      <layout class="QGridLayout" name="gridLayout">
       <item row="0" column="0">
        <widget class="QLineEdit" name="lineEdit"/>
       </item>
       <item row="1" column="0">
        <widget class="QLabel" name="label">
         <property name="text">
          <string>TextLabel</string>
         </property>
        </widget>
       </item>
       <item row="2" column="0">
        <widget class="QLineEdit" name="lineEdit_2"/>
       </item>
      </layout>
     </widget>
     <resources/>
     <connections>
      <connection>
       <sender>lineEdit</sender>
       <signal>textChanged(QString)</signal>
       <receiver>label</receiver>
       <slot>setText(QString)</slot>
       <hints>
        <hint type="sourcelabel">
         <x>228</x>
         <y>23</y>
        </hint>
        <hint type="destinationlabel">
         <x>37</x>
         <y>197</y>
        </hint>
       </hints>
      </connection>
     </connections>
    </ui>
    """
)


qmainwindow_ui = textwrap.dedent(
    """\
    <?xml version="1.0" encoding="UTF-8"?>
    <ui version="4.0">
     <class>MainWindow</class>
     <widget class="QMainWindow" name="MainWindow">
      <property name="geometry">
       <rect>
        <x>0</x>
        <y>0</y>
        <width>238</width>
        <height>44</height>
       </rect>
      </property>
      <property name="windowTitle">
       <string>MainWindow</string>
      </property>
      <widget class="QWidget" name="centralwidget">
       <layout class="QVBoxLayout" name="verticalLayout">
        <item>
         <widget class="QLineEdit" name="lineEdit"/>
        </item>
       </layout>
      </widget>
     </widget>
     <resources/>
     <connections/>
    </ui>
    """
)


qdialog_ui = textwrap.dedent(
    """\
    <?xml version="1.0" encoding="UTF-8"?>
    <ui version="4.0">
     <class>Dialog</class>
     <widget class="QDialog" name="Dialog">
      <property name="geometry">
       <rect>
        <x>0</x>
        <y>0</y>
        <width>186</width>
        <height>38</height>
       </rect>
      </property>
      <property name="windowTitle">
       <string>Dialog</string>
      </property>
      <layout class="QVBoxLayout" name="verticalLayout">
       <item>
        <widget class="QLineEdit" name="lineEdit"/>
       </item>
      </layout>
     </widget>
     <resources/>
     <connections/>
    </ui>
    """
)


qdockwidget_ui = textwrap.dedent(
    """\
    <?xml version="1.0" encoding="UTF-8"?>
    <ui version="4.0">
     <class>DockWidget</class>
     <widget class="QDockWidget" name="DockWidget">
      <property name="geometry">
       <rect>
        <x>0</x>
        <y>0</y>
        <width>169</width>
        <height>60</height>
       </rect>
      </property>
      <property name="windowTitle">
       <string>DockWidget</string>
      </property>
      <widget class="QWidget" name="dockWidgetContents">
       <layout class="QVBoxLayout" name="verticalLayout">
        <item>
         <widget class="QLineEdit" name="lineEdit"/>
        </item>
       </layout>
      </widget>
     </widget>
     <resources/>
     <connections/>
    </ui>
    """
)


qcustomwidget_ui = textwrap.dedent(
    """\
    <?xml version="1.0" encoding="UTF-8"?>
    <ui version="4.0">
     <class>MainWindow</class>
     <widget class="QMainWindow" name="MainWindow">
      <property name="geometry">
       <rect>
        <x>0</x>
        <y>0</y>
        <width>238</width>
        <height>44</height>
       </rect>
      </property>
      <property name="windowTitle">
       <string>MainWindow</string>
      </property>
      <widget class="CustomWidget" name="customwidget">
      </widget>
     </widget>
     <customwidgets>
      <customwidget>
       <class>CustomWidget</class>
       <extends>QWidget</extends>
       <header>tests.h</header>
      </customwidget>
     </customwidgets>
     <resources/>
     <connections/>
    </ui>
    """
)


qpycustomwidget_ui = textwrap.dedent(
    """\
    <?xml version="1.0" encoding="UTF-8"?>
    <ui version="4.0">
     <class>MainWindow</class>
     <widget class="QMainWindow" name="MainWindow">
      <property name="geometry">
       <rect>
        <x>0</x>
        <y>0</y>
        <width>238</width>
        <height>44</height>
       </rect>
      </property>
      <property name="windowTitle">
       <string>MainWindow</string>
      </property>
      <widget class="CustomWidget" name="customwidget">
      </widget>
     </widget>
     <customwidgets>
      <customwidget>
       <class>CustomWidget</class>
       <extends>QWidget</extends>
       <header>custom.customwidget.customwidget</header>
      </customwidget>
     </customwidgets>
     <resources/>
     <connections/>
    </ui>
    """
)


python_custom_widget = textwrap.dedent(
    '''
    def CustomWidget(parent=None):
        """
        Wrap CustomWidget class into a function to avoid global Qt import
        """
        from Qt import QtWidgets

        class Widget(QtWidgets.QWidget):
            pass

        return Widget(parent)
    '''
)


def setup():
    """Module-wide initialisation

    This function runs once, followed by teardown() below once
    all tests have completed.

    """
    self.tempdir = Path(tempfile.mkdtemp())

    def saveUiFile(filename, ui_template):
        filename = self.tempdir / filename
        with io.open(filename, "w", encoding="utf-8") as f:
            f.write(ui_template)
        return filename

    self.ui_qwidget = saveUiFile("qwidget.ui", qwidget_ui)
    self.ui_qmainwindow = saveUiFile("qmainwindow.ui", qmainwindow_ui)
    self.ui_qdialog = saveUiFile("qdialog.ui", qdialog_ui)
    self.ui_qdockwidget = saveUiFile("qdockwidget.ui", qdockwidget_ui)
    self.ui_qpycustomwidget = saveUiFile("qcustomwidget.ui", qcustomwidget_ui)


def setUpModule():
    """Module-wide initialisation

    This function runs once, followed by tearDownModule() below once
    all tests have completed.

    """
    setup()


def teardown():
    shutil.rmtree(self.tempdir)


def tearDownModule():
    teardown()


def binding(binding):
    """Isolate test to a particular binding

    When used, tests inside the if-statement are run independently
    with the given binding.

    Without this function, a test is run once for each binding.

    """

    return os.getenv("QT_PREFERRED_BINDING") == binding


def get_enum(cls, namespace, enum):
    """Get an enum from a fully qualified namespace

    Qt4 and older Qt5 don't support fully qualified enum names, this accounts
    for it.

    For example to access `Qt.QtCore.Qt.WindowState.WindowActive` using
    `get_enum(Qt.QtCore.Qt, "WindowState", "WindowActive")` returns
    `Qt.QtCore.Qt.WindowState.WindowActive` for newer Qt versions. For Qt
    versions that don't support fully qualified enum names it returns
    `Qt.QtCore.Qt.WindowActive`.

    Args:
        cls: The class that contains the enum.
        namespace(str): The namespace name in Qt6.
        enum(str): The name of the enum value.
    """
    if not hasattr(cls, namespace):
        # Legacy short enum name
        return getattr(cls, enum)
    namespace_cls = getattr(cls, namespace)
    if hasattr(namespace_cls, enum):
        # Return new fully qualified enum if possible
        return getattr(namespace_cls, enum)
    # Fallback to legacy short enum name if not using new enum classes
    return getattr(cls, enum)


def subprocess_run(cmd, **kwargs):
    """Work around python 3.7 not supporting passing pathlib objects to cmd.
    TODO: Remove once we drop python 3.7 support.
    """
    if sys.version_info < (3, 8) and not isinstance(cmd, str):
        cmd = [str(c) for c in cmd]
    return subprocess.run(cmd, **kwargs)


def subprocess_check_output(cmd, **kwargs):
    """Work around python 3.7 not supporting passing pathlib objects to cmd.
    TODO: Remove once we drop python 3.7 support.
    """
    if sys.version_info < (3, 8) and not isinstance(cmd, str):
        cmd = [str(c) for c in cmd]
    return subprocess.check_output(cmd, **kwargs)


@contextlib.contextmanager
def ignoreQtMessageHandler(msgs):
    """A context that ignores specific qMessages for all bindings

    Args:
        msgs: list of message strings to ignore
    """
    from Qt import QtCompat

    def messageOutputHandler(msgType, logContext, msg):
        if msg in msgs:
            return
        sys.stderr.write("{0}\n".format(msg))

    QtCompat.qInstallMessageHandler(messageOutputHandler)
    try:
        yield
    finally:
        QtCompat.qInstallMessageHandler(None)


def test_environment():
    """Tests require all bindings to be installed (except PySide on py3.5+)"""

    if sys.version_info >= (3, 11):
        # NOTE: Qt6 is only available for python 3.11 and above
        imp.find_module("PySide6")
        imp.find_module("PyQt6")
    else:
        imp.find_module("PySide2")
        imp.find_module("PyQt5")


def test_load_ui_returntype():
    """load_ui returns an instance of QObject"""

    import sys
    from Qt import QtWidgets, QtCore, QtCompat

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    obj = QtCompat.loadUi(self.ui_qwidget)
    assert isinstance(obj, QtCore.QObject)
    app.exit()


def test_load_ui_baseinstance():
    """Tests to see if the baseinstance loading loads a QWidget on properly"""
    import sys
    from Qt import QtWidgets, QtCompat

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    win = QtWidgets.QWidget()
    QtCompat.loadUi(self.ui_qwidget, win)
    assert hasattr(win, "lineEdit"), "loadUi could not load instance to win"
    app.exit()


def test_load_ui_signals():
    """Tests to see if the baseinstance connects signals properly"""
    import sys
    from Qt import QtWidgets, QtCompat

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    win = QtWidgets.QWidget()
    QtCompat.loadUi(self.ui_qwidget, win)

    win.lineEdit.setText("Hello")
    assert str(win.label.text()) == "Hello", "lineEdit signal did not fire"

    app.exit()


def test_load_ui_mainwindow():
    """Tests to see if the baseinstance loading loads a QMainWindow properly"""
    import sys
    from Qt import QtWidgets, QtCompat

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    win = QtWidgets.QMainWindow()

    QtCompat.loadUi(self.ui_qmainwindow, win)

    assert hasattr(win, "lineEdit"), "loadUi could not load instance to main window"

    app.exit()


def test_load_ui_dialog():
    """Tests to see if the baseinstance loading loads a QDialog properly"""
    import sys
    from Qt import QtWidgets, QtCompat

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    win = QtWidgets.QDialog()

    QtCompat.loadUi(self.ui_qdialog, win)

    assert hasattr(win, "lineEdit"), "loadUi could not load instance to main window"

    app.exit()


def test_load_ui_dockwidget():
    """Tests to see if the baseinstance loading loads a QDockWidget properly"""
    import sys
    from Qt import QtWidgets, QtCompat

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    win = QtWidgets.QDockWidget()

    QtCompat.loadUi(self.ui_qdockwidget, win)

    assert hasattr(win, "lineEdit"), "loadUi could not load instance to main window"

    app.exit()


def test_load_ui_customwidget():
    """Tests to see if loadUi loads a custom widget properly"""
    import sys
    from Qt import QtWidgets, QtCompat

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    win = QtWidgets.QMainWindow()

    QtCompat.loadUi(self.ui_qpycustomwidget, win)

    # Ensure that the derived class was properly created
    # and not the base class (in case of failure)
    custom_class_name = getattr(win, "customwidget", None).__class__.__name__
    excepted_class_name = CustomWidget(win).__class__.__name__
    assert custom_class_name == excepted_class_name, (
        "loadUi could not load custom widget to main window"
    )

    app.exit()


def test_load_ui_pycustomwidget():
    """Tests to see if loadUi loads a custom widget properly"""
    import sys
    from Qt import QtWidgets, QtCompat

    # create a python file for the custom widget in a directory relative to the tempdir
    filename = self.tempdir / "custom" / "customwidget" / "customwidget.py"
    filename.parent.mkdir(parents=True)
    with io.open(filename, "w", encoding="utf-8") as f:
        f.write(self.python_custom_widget)

    # Python 2.7 requires that each folder be a package
    with io.open(self.tempdir / "custom" / "__init__.py", "w", encoding="utf-8") as f:
        f.write("")
    with io.open(
        self.tempdir / "custom" / "customwidget" / "__init__.py", "w", encoding="utf-8"
    ) as f:
        f.write("")
    # append the path to ensure the future import can be loaded 'relative' to the tempdir
    sys.path.append(str(self.tempdir))

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()

    win = QtWidgets.QMainWindow()

    QtCompat.loadUi(self.ui_qpycustomwidget, win)

    # Ensure that the derived class was properly created
    # and not the base class (in case of failure)
    custom_class_name = getattr(win, "customwidget", None).__class__.__name__
    excepted_class_name = CustomWidget(win).__class__.__name__
    assert custom_class_name == excepted_class_name, (
        "loadUi could not load custom widget to main window"
    )

    app.exit()


def test_load_ui_invalidpath():
    """Tests to see if loadUi successfully fails on invalid paths"""
    import sys
    from Qt import QtWidgets, QtCompat

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    assert_raises(IOError, QtCompat.loadUi, "made/up/path")
    app.exit()


def test_load_ui_invalidxml():
    """Tests to see if loadUi successfully fails on invalid ui files"""
    import sys

    invalid_xml = self.tempdir / "invalid.ui"
    with io.open(invalid_xml, "w", encoding="utf-8") as f:
        f.write("""
        <?xml version="1.0" encoding="UTF-8"?>
        <ui version="4.0" garbage
        </ui>
        """)

    from xml.etree import ElementTree
    from Qt import QtWidgets, QtCompat

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    assert_raises(ElementTree.ParseError, QtCompat.loadUi, invalid_xml)
    app.exit()


def test_load_ui_existingLayoutOnDialog():
    """Tests to see if loading a ui onto a layout in a Dialog works"""
    import sys
    from Qt import QtWidgets, QtCompat

    msgs = (
        'QLayout: Attempting to add QLayout "" to QDialog '
        '"Dialog", which already has a layout'
    )

    with ignoreQtMessageHandler([msgs]):
        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()
        win = QtWidgets.QDialog()
        QtWidgets.QComboBox(win)
        QtWidgets.QHBoxLayout(win)
        QtCompat.loadUi(self.ui_qdialog, win)
    app.exit()


def test_load_ui_existingLayoutOnMainWindow():
    """Tests to see if loading a ui onto a layout in a MainWindow works"""
    import sys
    from Qt import QtWidgets, QtCompat

    msgs = (
        'QLayout: Attempting to add QLayout "" to QMainWindow '
        '"", which already has a layout'
    )

    with ignoreQtMessageHandler([msgs]):
        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()
        win = QtWidgets.QMainWindow()
        QtWidgets.QComboBox(win)
        QtWidgets.QHBoxLayout(win)
        QtCompat.loadUi(self.ui_qmainwindow, win)
    app.exit()


def test_load_ui_existingLayoutOnDockWidget():
    """Tests to see if loading a ui onto a layout in a DockWidget works"""
    import sys
    from Qt import QtWidgets, QtCompat

    msgs = (
        'QLayout: Attempting to add QLayout "" to QDockWidget '
        '"", which already has a layout'
    )

    with ignoreQtMessageHandler([msgs]):
        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()
        win = QtWidgets.QDockWidget()
        QtWidgets.QComboBox(win)
        QtWidgets.QHBoxLayout(win)
        QtCompat.loadUi(self.ui_qdockwidget, win)
    app.exit()


def test_load_ui_existingLayoutOnWidget():
    """Tests to see if loading a ui onto a layout in a Widget works"""
    import sys
    from Qt import QtWidgets, QtCompat

    msgs = (
        'QLayout: Attempting to add QLayout "" to QWidget '
        '"Form", which already has a layout'
    )

    with ignoreQtMessageHandler([msgs]):
        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()
        win = QtWidgets.QWidget()
        QtWidgets.QComboBox(win)
        QtWidgets.QHBoxLayout(win)
        QtCompat.loadUi(self.ui_qwidget, win)
    app.exit()


def test_preferred_none():
    """Preferring None shouldn't import anything"""

    current = os.environ["QT_PREFERRED_BINDING"]
    try:
        os.environ["QT_PREFERRED_BINDING"] = "None"
        import Qt

        assert Qt.__name__ == "Qt", Qt
    finally:
        os.environ["QT_PREFERRED_BINDING"] = current


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

    project = self.tempdir / "myproject"
    vendor = project / "vendor"

    vendor.mkdir(parents=True)

    # Make packages out of folders
    with (project / "__init__.py").open("w") as f:
        f.write("from .vendor.Qt import QtWidgets")

    with (vendor / "__init__.py").open("w") as f:
        f.write("\n")

    # Copy real Qt.py into myproject
    shutil.copy(REPO_ROOT / "src" / "Qt.py", vendor / "Qt.py")

    # Copy real Qt.py into the root folder
    shutil.copy(REPO_ROOT / "src" / "Qt.py", self.tempdir / "Qt.py")

    print("Testing relative import..")
    assert (
        subprocess.call(
            [sys.executable, "-c", "import myproject"],
            cwd=self.tempdir,
            stdout=subprocess.PIPE,  # With nose process isolation, buffer can
            stderr=subprocess.STDOUT,  # easily get full and throw an error.
        )
        == 0
    )

    print("Testing absolute import..")
    assert (
        subprocess.call(
            [sys.executable, "-c", "from myproject.vendor.Qt import QtWidgets"],
            cwd=self.tempdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        == 0
    )

    print("Testing direct import..")
    assert (
        subprocess.call(
            [sys.executable, "-c", "import myproject.vendor.Qt"],
            cwd=self.tempdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        == 0
    )

    #
    # Test invalid json data
    print("Testing invalid json data..")
    env = os.environ.copy()
    env["QT_PREFERRED_BINDING_JSON"] = '{"Qt":["PyQt6","PyQt5"],}'

    cmd = "import myproject.vendor.Qt;"
    cmd += "import Qt;"
    cmd += "assert myproject.vendor.Qt.__binding__ != None, 'vendor';"
    cmd += "assert Qt.__binding__ != None, 'Qt';"

    popen = subprocess.Popen(
        [sys.executable, "-c", cmd],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=self.tempdir,
        env=env,
    )

    out, err = popen.communicate()

    if popen.returncode != 0:
        print(out)
        msg = "An exception was raised"
        assert popen.returncode == 0, msg

    error_check = b"Qt.py [warning]:"
    assert err.startswith(error_check), err

    print("out------------------")
    print(out)

    print("err ------------------")
    print(err)

    # Check QT_PREFERRED_BINDING_JSON works as expected
    print("Testing QT_PREFERRED_BINDING_JSON is respected..")
    cmd = "import myproject.vendor.Qt;"
    # Check that the "None" binding was set for `import myproject.vendor.Qt`
    cmd += "assert myproject.vendor.Qt.__binding__ == 'None', 'vendor';"
    cmd += "import Qt;"
    # Check that the "None" binding was not set for `import Qt`.
    # This should be PyQt6 or PyQt5 depending on the test environment.
    cmd += "assert Qt.__binding__ != 'None', 'Qt'"

    # If the module name is "Qt" use PyQt6 or PyQt5, otherwise use None binding
    env = os.environ.copy()
    env["QT_PREFERRED_BINDING_JSON"] = json.dumps(
        {"Qt": ["PySide6", "PyQt5"], "default": ["None"]}
    )

    assert (
        subprocess.call(
            [sys.executable, "-c", cmd],
            stdout=subprocess.PIPE,
            cwd=self.tempdir,
            env=env,
        )
        == 0
    )

    print("Testing QT_PREFERRED_BINDING_JSON and QT_PREFERRED_BINDING work..")
    env["QT_PREFERRED_BINDING_JSON"] = '{"Qt":["PySide6","PyQt5"]}'
    env["QT_PREFERRED_BINDING"] = "None"
    assert (
        subprocess.call(
            [sys.executable, "-c", cmd],
            stdout=subprocess.PIPE,
            cwd=self.tempdir,
            env=env,
        )
        == 0
    )


def test_convert_simple():
    """python -m Qt --convert works in general"""
    before = textwrap.dedent(
        """\
        from PySide2 import QtCore, QtGui, QtWidgets

        class Ui_uic(object):
            def setupUi(self, uic):
                self.retranslateUi(uic)

            def retranslateUi(self, uic):
                self.pushButton_2.setText(
                    QtWidgets.QApplication.translate("uic", "NOT Ok", None, -1))
        """
    )

    after = textwrap.dedent(
        """\
        from Qt import QtCore, QtGui, QtWidgets
        from Qt import QtCompat

        class Ui_uic(object):
            def setupUi(self, uic):
                self.retranslateUi(uic)

            def retranslateUi(self, uic):
                self.pushButton_2.setText(
                    QtCompat.translate("uic", "NOT Ok", None, -1))
        """
    )

    fname = self.tempdir / "simple.py"
    with fname.open("w") as f:
        f.write(before)

    from Qt import QtCompat

    current_dir = os.getcwd()
    os.chdir(self.tempdir)
    QtCompat._cli(args=["--convert", "simple.py"])

    with fname.open() as f:
        assert f.read() == after

    # Prevent windows file lock PermissionError issues when testing on windows.
    os.chdir(current_dir)


def test_convert_5_15_2_format():
    before = textwrap.dedent(
        """\
        from PySide2.QtCore import *
        from PySide2.QtGui import *
        from PySide2.QtWidgets import *

        class Ui_uic(object):
            def setupUi(self, uic):
                self.retranslateUi(uic)

            def retranslateUi(self, uic):
                self.pushButton_2.setText(
                    QCoreApplication.translate("uic", "NOT Ok", None, -1))
            """
    )

    after = textwrap.dedent(
        """\
        from Qt.QtCore import *
        from Qt.QtGui import *
        from Qt.QtWidgets import *
        from Qt import QtCompat

        class Ui_uic(object):
            def setupUi(self, uic):
                self.retranslateUi(uic)

            def retranslateUi(self, uic):
                self.pushButton_2.setText(
                    QtCompat.translate("uic", "NOT Ok", None, -1))
            """
    )

    fname = self.tempdir / "5_15_2_uic.py"
    with fname.open("w") as f:
        f.write(before)

    from Qt import QtCompat

    current_dir = os.getcwd()
    os.chdir(self.tempdir)
    QtCompat._cli(args=["--convert", "5_15_2_uic.py"])

    with fname.open() as f:
        assert f.read() == after

    # Prevent windows file lock PermissionError issues when testing on windows.
    os.chdir(current_dir)


def test_convert_idempotency():
    """Converting a converted file produces an identical file"""
    before = textwrap.dedent(
        """\
        from PySide2 import QtCore, QtGui, QtWidgets

        class Ui_uic(object):
            def setupUi(self, uic):
                self.retranslateUi(uic)

            def retranslateUi(self, uic):
                self.pushButton_2.setText(
                    QtWidgets.QApplication.translate("uic", "NOT Ok", None, -1))
        """
    )

    after = textwrap.dedent(
        """\
        from Qt import QtCore, QtGui, QtWidgets
        from Qt import QtCompat

        class Ui_uic(object):
            def setupUi(self, uic):
                self.retranslateUi(uic)

            def retranslateUi(self, uic):
                self.pushButton_2.setText(
                    QtCompat.translate("uic", "NOT Ok", None, -1))
        """
    )

    fname = self.tempdir / "idempotency.py"
    with fname.open("w") as f:
        f.write(before)

    from Qt import QtCompat

    current_dir = os.getcwd()
    os.chdir(self.tempdir)
    QtCompat._cli(args=["--convert", "idempotency.py"])

    with fname.open() as f:
        assert f.read() == after

    QtCompat._cli(args=["--convert", "idempotency.py"])

    with fname.open() as f:
        assert f.read() == after

    # Prevent windows file lock PermissionError issues when testing on windows.
    os.chdir(current_dir)


def test_convert_backup():
    """Converting produces a backup"""

    fname = self.tempdir / "idempotency.py"
    with fname.open("w") as f:
        f.write("")

    from Qt import QtCompat

    current_dir = os.getcwd()
    os.chdir(self.tempdir)
    QtCompat._cli(args=["--convert", "idempotency.py"])

    assert (self.tempdir / f"{fname.stem}_backup{fname.suffix}").exists()

    # Prevent windows file lock PermissionError issues when testing on windows.
    os.chdir(current_dir)


def test_import_from_qtwidgets():
    """Fix #133, `from Qt.QtWidgets import XXX` works"""
    from Qt.QtWidgets import QPushButton

    assert QPushButton.__name__ == "QPushButton", QPushButton


def test_import_from_qtcompat():
    """`from Qt.QtCompat import XXX` works"""
    from Qt.QtCompat import loadUi

    assert loadUi.__name__ == "_loadUi", loadUi


def test_i158_qtcore_direct_import():
    """import Qt.QtCore works on all bindings

    This addresses issue #158

    """

    import Qt.QtCore

    assert hasattr(Qt.QtCore, "Signal")


def test_translate_arguments():
    """Arguments of QtCompat.translate are correct

    QtCompat.translate is a shim over the PyQt6 and PyQt5
    equivalent with an interface like the one found in PySide2.

    Reference: https://doc.qt.io/qt-5/qcoreapplication.html#translate

    """

    import Qt

    # This will run on each binding
    result = Qt.QtCompat.translate(
        "CustomDialog",  # context
        "Status",  # sourceText
        None,  # disambiguation
        -1,
    )  # n
    assert result == "Status", result


def test_binding_and_qt_version():
    """Qt's __binding_version__ and __qt_version__ populated"""

    import Qt

    assert Qt.__binding_version__ != "0.0.0", "Binding version was not populated"
    assert Qt.__qt_version__ != "0.0.0", "Qt version was not populated"


def test_binding_states():
    """Tests to see if the Qt binding enum states are set properly"""
    import Qt

    assert Qt.IsPySide is False
    assert Qt.IsPySide2 == binding("PySide2")
    assert Qt.IsPySide6 == binding("PySide6")
    if sys.version_info >= (3, 9):
        # NOTE: Existing docker images don't support Qt6
        assert Qt.IsPyQt6 == binding("PyQt6")
    assert Qt.IsPyQt5 == binding("PyQt5")
    assert Qt.IsPyQt4 is False


def test_qtcompat_base_class():
    """Tests to ensure the QtCompat namespace object works as expected"""
    import sys
    import Qt
    from Qt import QtWidgets
    from Qt import QtCompat

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()  # noqa: F841
    header = QtWidgets.QHeaderView(get_enum(Qt.QtCore.Qt, "Orientation", "Horizontal"))

    # Spot check compatibility functions
    QtCompat.QHeaderView.setSectionsMovable(header, False)
    assert QtCompat.QHeaderView.sectionsMovable(header) is False
    QtCompat.QHeaderView.setSectionsMovable(header, True)
    assert QtCompat.QHeaderView.sectionsMovable(header) is True

    # Verify that the grab function actually generates a non-null image
    button = QtWidgets.QPushButton("TestImage")
    pixmap = QtCompat.QWidget.grab(button)
    assert not pixmap.isNull()


def test_cli():
    """Qt.py is available from the command-line"""
    env = os.environ.copy()
    env.pop("QT_VERBOSE")  # Do not include debug messages

    popen = subprocess.Popen(
        [sys.executable, "src/Qt.py", "--help"], stdout=subprocess.PIPE, env=env
    )

    out, err = popen.communicate()
    assert out.startswith(b"usage: Qt.py"), "\n%s" % out


def test_membership():
    """Common members of Qt.py exist in all bindings.

    Checks against the `.members/common_members.json` file generated by running
    tox's membership-* tests. These must be run before running this test
    creating that file. This test checks that Qt._common_members matches this
    file.
    """
    import Qt

    common_members = Qt._common_members.copy()

    ref_path = REPO_ROOT / ".members" / "common_members.json"
    assert ref_path.exists(), (
        "This test requires the files generated by the `tox membership-*` "
        "tests. Run those tests first."
    )
    ref_members = json.load(ref_path.open()).get("members", {})

    missing = []
    for module, members in common_members.items():
        ref_module = ref_members[module]
        for member in members:
            # Verify that all members defined in Qt's common_members are found
            # in the current tox generated common_members.json.
            if hasattr(getattr(Qt, module), member):
                assert member in ref_module, (
                    f"Qt.{module}.{member} missing from '{ref_path}'"
                )
                # remove this member from the reference
                ref_module.remove(member)
            else:
                missing.append(member)
        # remove ref_module if its empty
        if not ref_module:
            ref_members.pop(module)

    binding = Qt.__binding__
    assert not missing, "Some members did not exist in {binding}\n{missing}".format(
        **locals()
    )

    # Check that all members specified in common_members.json are found in
    # Qt._common_members
    assert not ref_members, (
        f"Extra members found in '{ref_path}' that are not in "
        f"Qt._common_members. Remaining: {ref_members}"
    )


def test_misplaced():
    """Verify that misplaced members are present in all places"""
    import Qt

    assert Qt.QtWidgets.QFileSystemModel
    # QAction was moved, then moved back. Qt.py exposes both places
    assert Qt.QtGui.QAction
    assert Qt.QtGui.QAction == Qt.QtWidgets.QAction


def test__extras__():
    """Spot check binding specific imports for missing members.

    This should check at least one import for each common member that requires
    being added to any bindings `__extras__` list.
    """
    import Qt

    assert Qt.QtOpenGL.QAbstractOpenGLFunctions
    assert Qt.QtOpenGL.QOpenGLBuffer
    assert Qt.QtOpenGL.QOpenGLFunctions_2_0
    assert Qt.QtOpenGL.QOpenGLFunctions_2_1
    assert Qt.QtOpenGL.QOpenGLFunctions_4_1_Core


def test__extras__none():
    """Preferring None should add the __extras__ modules"""

    current = os.environ["QT_PREFERRED_BINDING"]
    try:
        os.environ["QT_PREFERRED_BINDING"] = "None"
        import Qt

        assert Qt.QtOpenGL
    finally:
        os.environ["QT_PREFERRED_BINDING"] = current


def test_missing():
    """Missing members of Qt.py have been defined with placeholders"""
    import Qt

    missing_members = Qt._missing_members.copy()

    missing = []
    for module, members in missing_members.items():
        mod = getattr(Qt, module)
        missing.extend(
            member
            for member in members
            if not hasattr(mod, member)
            or not isinstance(getattr(mod, member), Qt.MissingMember)
        )

    binding = Qt.__binding__
    assert not missing, (
        "Some members did not exist in {binding} as "
        "a Qt.MissingMember type\n{missing}".format(**locals())
    )


def test_unicode_error_messages():
    """Test if unicode error messages with non-ascii characters
    throw the error reporter off"""
    import Qt

    unicode_message = "DLL load failed : le module spécifié est introuvable."
    str_message = "DLL load failed : le module"

    with captured_output() as out:
        stdout, stderr = out
        Qt._warn(text=unicode_message)
        assert str_message in stderr.getvalue()


def test_enum_value():
    """Test QtCompat.enumValue returns an int value."""
    from Qt import QtCompat, QtGui
    from Qt.QtCore import Qt

    # Get the enum objects to test with
    enum_window_active = get_enum(Qt, "WindowState", "WindowActive")
    enum_demi_bold = get_enum(QtGui.QFont, "Weight", "DemiBold")

    if binding("PySide6") or binding("PyQt6"):
        window_active_check = enum_window_active.value
        # Note: Both int and .value work for this enum
        demi_bold_check = enum_demi_bold.value
    else:
        window_active_check = int(enum_window_active)
        demi_bold_check = int(enum_demi_bold)

    assert QtCompat.enumValue(enum_window_active) == window_active_check
    assert QtCompat.enumValue(enum_demi_bold) == demi_bold_check
    assert isinstance(QtCompat.enumValue(enum_window_active), int)
    assert isinstance(QtCompat.enumValue(enum_demi_bold), int)


def test_qfont_from_string():
    import Qt

    enum_weight_normal = get_enum(Qt.QtGui.QFont, "Weight", "Normal")
    enum_weight_bold = get_enum(Qt.QtGui.QFont, "Weight", "Bold")

    in_font = "Arial,7,-1,5,400,0,0,0,0,0,0,0,0,0,0,1"
    # PyQt5 for Python 3.7 requires creating a QApplication to init a QFont
    if binding("PyQt5"):
        if not Qt.QtWidgets.QApplication.instance():
            app = Qt.QtWidgets.QApplication(sys.argv)
        else:
            app = Qt.QtWidgets.QApplication.instance()
    try:
        font = Qt.QtGui.QFont()
        Qt.QtCompat.QFont.fromString(font, in_font)
        assert font.family() == "Arial"
        assert font.pointSizeF() == 7.0
        assert font.weight() == enum_weight_normal
        font.setWeight(enum_weight_bold)
        if binding("PySide6") or binding("PyQt6"):
            # In Qt6 the full string is returned with OpenType weight of 700
            out_font = "Arial,7,-1,5,700,0,0,0,0,0,0,0,0,0,0,1"
            assert font.toString() == out_font
        else:
            # In previous bindings the shorter version is returned. Also the bold
            # weight is 75 instead of 700
            assert font.toString() == "Arial,7,-1,5,75,0,0,0,0,0"
    finally:
        if binding("PyQt5"):
            app.exit()


if binding("PyQt6"):

    def test_preferred_pyqt6():
        """QT_PREFERRED_BINDING = PyQt6 properly forces the binding"""
        import Qt

        assert Qt.__binding__ == "PyQt6", (
            "PyQt6 should have been picked, instead got %s" % Qt.__binding__
        )


if binding("PyQt5"):

    def test_preferred_pyqt5():
        """QT_PREFERRED_BINDING = PyQt5 properly forces the binding"""
        import Qt

        assert Qt.__binding__ == "PyQt5", (
            "PyQt5 should have been picked, instead got %s" % Qt.__binding__
        )


if binding("PySide2"):

    def test_preferred_pyside2():
        """QT_PREFERRED_BINDING = PySide2 properly forces the binding"""
        import Qt

        assert Qt.__binding__ == "PySide2", (
            "PySide2 should have been picked, instead got %s" % Qt.__binding__
        )

    def test_coexistence():
        """Qt.py may be use alongside the actual binding"""

        from Qt import QtCore
        import PySide2.QtGui

        # Qt remaps QStringListModel
        assert QtCore.QStringListModel

        # But does not delete the original. Older versions of PySide2 had this
        # on QtGui instead of QtCore
        assert hasattr(PySide2.QtCore, "QStringListModel") or hasattr(
            PySide2.QtGui, "QStringListModel"
        )


if binding("PySide6"):

    def test_preferred_pyside6():
        """QT_PREFERRED_BINDING = PySide6 properly forces the binding"""
        import Qt

        assert Qt.__binding__ == "PySide6", (
            "PySide6 should have been picked, instead got %s" % Qt.__binding__
        )

    def test_coexistence():
        """Qt.py may be use alongside the actual binding"""

        from Qt import QtCore
        import PySide6.QtCore

        # Qt remaps QStringListModel
        assert QtCore.QStringListModel

        # But does not delete the original
        assert PySide6.QtCore.QStringListModel


if binding("PyQt5") or binding("PyQt6") and sys.version_info < (3, 11):
    # NOTE: If using python 3.11+ PyQt5 is not available.
    def test_multiple_preferred():
        """QT_PREFERRED_BINDING = more than one binding excludes others"""

        # PySide is the more desirable binding
        current = os.environ["QT_PREFERRED_BINDING"]
        try:
            os.environ["QT_PREFERRED_BINDING"] = os.pathsep.join(["PyQt5", "PyQt6"])
            import Qt

            assert Qt.__binding__ == "PyQt5", (
                "PyQt5 should have been picked, instead got %s" % Qt.__binding__
            )
        finally:
            os.environ["QT_PREFERRED_BINDING"] = current


enum_file_1 = textwrap.dedent(
    """
    # a comment Qt.WindowActive with an enum. This file uses enums from super-classes
    if QAbstractItemView.Box:
        print(QTreeWidget.Box)
        print(QFrame.Box)
        # Note: Not using a Qt class so this will only be found by the --partial check
        self.Box
    """
)


enum_file_2 = textwrap.dedent(
    """
    # a comment QStyle.CC_ComboBox that has a enum in it
    print(QFrame.Box)
    print(self.Box)
    """
)


enum_check = textwrap.dedent(
    """\
    '__init__.py': Replace 'Qt.WindowActive' => 'Qt.WindowState.WindowActive' (1)
    '__init__.py': Replace 'QAbstractItemView.Box' => 'QAbstractItemView.Shape.Box' (1)
    '__init__.py': Replace 'QFrame.Box' => 'QFrame.Shape.Box' (1)
    '__init__.py': Replace 'QTreeWidget.Box' => 'QTreeWidget.Shape.Box' (1)
    'api{slash}example.py': Replace 'QFrame.Box' => 'QFrame.Shape.Box' (1)
    'api{slash}example.py': Replace 'QStyle.CC_ComboBox' => 'QStyle.ComplexControl.CC_ComboBox' (1)
    """
)
enum_check = enum_check.format(slash=os.sep)


if binding("PySide2"):

    def test_convert_enum():
        """Test the output of running Qt_convert_enum.py."""

        code_path = REPO_ROOT / "src" / "Qt_convert_enum.py"
        old_code_dir = self.tempdir / "enum_convert"
        api_dir = old_code_dir / "api"
        init_file = old_code_dir / "__init__.py"
        example_file = api_dir / "example.py"
        api_dir.mkdir(parents=True)

        # Test the dry run mode text output
        with init_file.open("w") as fle:
            fle.write(enum_file_1)

        with open(example_file, "w") as fle:
            fle.write(enum_file_2)

        cmd = [sys.executable, code_path, old_code_dir]
        output = subprocess_check_output(cmd, cwd=self.tempdir, universal_newlines=True)

        assert enum_check in output

        # Check using the "--check" command outputs the same text but uses
        # the return code for the number of enums being changed.
        try:
            output = subprocess_check_output(
                cmd + ["--check"], cwd=self.tempdir, universal_newlines=True
            )
        except subprocess.CalledProcessError as error:
            assert error.returncode == 6
            assert error.stdout == output
            # The number of changes are added to the end of the output
            assert "6 enums require changes." in output

        # Test actually updating the files.
        cmd.append("--write")
        output = subprocess_check_output(cmd, cwd=self.tempdir, universal_newlines=True)
        assert enum_check in output

        # "--check" is respected in --write mode
        try:
            output = subprocess_check_output(
                cmd + ["--check"], cwd=self.tempdir, universal_newlines=True
            )
        except subprocess.CalledProcessError as error:
            assert error.returncode == 6
            assert error.stdout == output
            # The number of changes are added to the end of the output
            assert "6 enums changed." in output

        check = enum_file_1.replace("WindowActive", "WindowState.WindowActive")
        name_re = re.compile(r"(?<!self)\.Box")
        check = name_re.sub(".Shape.Box", check)
        with init_file.open() as fle:
            assert fle.read() == check

        check = enum_file_2.replace("CC_ComboBox", "ComplexControl.CC_ComboBox")
        check = name_re.sub(".Shape.Box", check)
        with open(example_file) as fle:
            assert fle.read() == check

        # Check using `--partial`
        output = subprocess_check_output(
            cmd + ["--partial", "-v"], cwd=self.tempdir, universal_newlines=True
        )
        check = textwrap.dedent(
            """\
            File: "__init__.py", line:7, for Box
                self.Box
            File: "api{slash}example.py", line:4, for Box
                print(self.Box)
            2 partial enums found.
            """
        ).format(slash=os.sep)
        assert output == check

    def test_convert_enum_map():
        """Test enum map generation for conversion from short to long enums"""
        code_path = REPO_ROOT / "src" / "Qt_convert_enum.py"
        cmd = [sys.executable, code_path, "--show", "map"]
        proc = subprocess_run(
            cmd,
            stdout=subprocess.PIPE,
            check=True,
            stderr=subprocess.DEVNULL,
            cwd=self.tempdir,
            universal_newlines=True,
        )

        data = json.loads(proc.stdout)
        assert data["Qt.WindowActive"] == "Qt.WindowState.WindowActive"
        assert data["QAbstractItemView.Box"] == "QAbstractItemView.Shape.Box"
        assert data["QFrame.Box"] == "QFrame.Shape.Box"
        assert data["QTreeWidget.Box"] == "QTreeWidget.Shape.Box"
        assert data["QFrame.Box"] == "QFrame.Shape.Box"
        assert data["QStyle.CC_ComboBox"] == "QStyle.ComplexControl.CC_ComboBox"

    def test_convert_enum_modules():
        """Test enum map generation modules data structure"""
        code_path = REPO_ROOT / "src" / "Qt_convert_enum.py"
        cmd = [sys.executable, code_path, "--show", "modules"]
        proc = subprocess_run(
            cmd,
            stdout=subprocess.PIPE,
            check=True,
            stderr=subprocess.DEVNULL,
            cwd=self.tempdir,
            universal_newlines=True,
        )

        data = json.loads(proc.stdout)
        assert data["QtCore"]["Qt.WindowActive"] == ["Qt.WindowState.WindowActive"]
        assert data["QtWidgets"]["QAbstractItemView.Box"] == [
            "QAbstractItemView.Shape.Box"
        ]
        assert data["QtWidgets"]["QFrame.Box"] == ["QFrame.Shape.Box"]
        assert data["QtWidgets"]["QTreeWidget.Box"] == ["QTreeWidget.Shape.Box"]
        assert data["QtWidgets"]["QFrame.Box"] == ["QFrame.Shape.Box"]
        assert data["QtWidgets"]["QStyle.CC_ComboBox"] == [
            "QStyle.ComplexControl.CC_ComboBox"
        ]


if binding("PySide6") and sys.version_info >= (3, 7):
    # Qt_convert_enum.py only runs in python 3.7 or higher
    def test_convert_enum_duplicates():
        """Tests using PySide6 to show enums with duplicate short names"""
        code_path = REPO_ROOT / "src" / "Qt_convert_enum.py"
        cmd = [sys.executable, code_path, "--show", "dups"]
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            check=True,
            stderr=subprocess.DEVNULL,
            cwd=self.tempdir,
            universal_newlines=True,
        )

        data = json.loads(proc.stdout)

        # Test some know duplicate enum values
        assert "PySide6" in data["BINDING_INFO"]
        assert data["QtGui"]["QColorSpace"]["AdobeRgb"] == [
            "NamedColorSpace.AdobeRgb, 3",
            "Primaries.AdobeRgb, 2",
        ]
