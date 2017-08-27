"""Tests that run once"""
import io
import os
import sys
import imp
import shutil
import tempfile
import subprocess
import contextlib

# Third-party dependency
import six

from nose.tools import (
    assert_raises,
)

PYTHON = sys.version_info[0]  # e.g. 2 or 3

try:
    long
except NameError:
    # Python 3 compatibility
    long = int


@contextlib.contextmanager
def captured_output():
    new_out, new_err = six.StringIO(), six.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


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
    """Tests require all bindings to be installed (except PySide on py3.5+)"""

    if sys.version_info <= (3, 4):
        # PySide is not available for Python > 3.4
        imp.find_module("PySide")
    imp.find_module("PySide2")
    imp.find_module("PyQt4")
    imp.find_module("PyQt5")


def test_load_ui_returntype():
    """load_ui returns an instance of QObject"""

    import sys
    from Qt import QtWidgets, QtCore, QtCompat
    app = QtWidgets.QApplication(sys.argv)
    obj = QtCompat.loadUi(self.ui_qwidget)
    assert isinstance(obj, QtCore.QObject)
    app.exit()


def test_load_ui_baseinstance():
    """Tests to see if the baseinstance loading loads widgets on properly"""
    import sys
    from Qt import QtWidgets, QtCompat
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QWidget()
    QtCompat.loadUi(self.ui_qwidget, win)
    assert hasattr(win, 'lineEdit'), "loadUi could not load instance to win"
    app.exit()


def test_load_ui_signals():
    """Tests to see if the baseinstance loading loads widgets on properly"""
    import sys
    from Qt import QtWidgets, QtCompat
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QWidget()
    QtCompat.loadUi(self.ui_qwidget, win)

    win.lineEdit.setText('Hello')
    assert str(win.label.text()) == 'Hello', "lineEdit signal did not fire"

    app.exit()


def test_load_ui_invalidpath():
    """Tests to see if loadUi successfully fails on invalid paths"""
    import sys
    from Qt import QtWidgets, QtCompat
    app = QtWidgets.QApplication(sys.argv)
    assert_raises(IOError, QtCompat.loadUi, 'made/up/path')
    app.exit()


def test_load_ui_invalidxml():
    """Tests to see if loadUi successfully fails on invalid ui files"""
    import sys
    invalid_xml = os.path.join(self.tempdir, "invalid.ui")
    with io.open(invalid_xml, "w", encoding="utf-8") as f:
        f.write(u"""
        <?xml version="1.0" encoding="UTF-8"?>
        <ui version="4.0" garbage
        </ui>
        """)

    from xml.etree import ElementTree
    from Qt import QtWidgets, QtCompat
    app = QtWidgets.QApplication(sys.argv)
    assert_raises(ElementTree.ParseError, QtCompat.loadUi, invalid_xml)
    app.exit()


def test_load_ui_overwrite_fails():
    """PyQt4/5 loadUi functiion will fail if the widget has a preexisting
    layout. This tests that our custom implementation for PySide does the same
    """
    import sys
    from Qt import QtWidgets, QtCompat
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(win)
    win.lineEdit = QtWidgets.QPushButton('Test')
    layout.addWidget(win.lineEdit)
    assert_raises(RuntimeError, QtCompat.loadUi, self.ui_qwidget, win)
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
        stdout=subprocess.PIPE,  # With nose process isolation, buffer can
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
""".split("\n")

    after = """\
from Qt import QtCompat, QtCore, QtGui, QtWidgets

class Ui_uic(object):
    def setupUi(self, uic):
        self.retranslateUi(uic)

    def retranslateUi(self, uic):
        self.pushButton_2.setText(
            QtCompat.translate("uic", "NOT Ok", None, -1))
""".split("\n")

    from Qt import QtCompat
    assert QtCompat._convert(before) == after, after


def test_convert_idempotency():
    """Converting a converted file produces an identical file"""
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
from Qt import QtCompat, QtCore, QtGui, QtWidgets

class Ui_uic(object):
    def setupUi(self, uic):
        self.retranslateUi(uic)

    def retranslateUi(self, uic):
        self.pushButton_2.setText(
            QtCompat.translate("uic", "NOT Ok", None, -1))
"""

    fname = os.path.join(self.tempdir, "idempotency.py")
    with open(fname, "w") as f:
        f.write(before)

    from Qt import QtCompat

    os.chdir(self.tempdir)
    QtCompat._cli(args=["--convert", "idempotency.py"])

    with open(fname) as f:
        assert f.read() == after

    QtCompat._cli(args=["--convert", "idempotency.py"])

    with open(fname) as f:
        assert f.read() == after


def test_convert_backup():
    """Converting produces a backup"""

    fname = os.path.join(self.tempdir, "idempotency.py")
    with open(fname, "w") as f:
        f.write("")

    from Qt import QtCompat

    os.chdir(self.tempdir)
    QtCompat._cli(args=["--convert", "idempotency.py"])

    assert os.path.exists(
        os.path.join(self.tempdir, "%s_backup%s" % os.path.splitext(fname))
    )


def test_import_from_qtwidgets():
    """Fix #133, `from Qt.QtWidgets import XXX` works"""
    from Qt.QtWidgets import QPushButton
    assert QPushButton.__name__ == "QPushButton", QPushButton


def test_i158_qtcore_direct_import():
    """import Qt.QtCore works on all bindings

    This addresses issue #158

    """

    import Qt.QtCore
    assert hasattr(Qt.QtCore, "Signal")


def test_translate_arguments():
    """Arguments of QtCompat.translate are correct

    QtCompat.translate is a shim over the PySide, PyQt4 and PyQt5
    equivalent with an interface like the one found in PySide2.

    Reference: https://doc.qt.io/qt-5/qcoreapplication.html#translate

    """

    import Qt

    # This will run on each binding
    result = Qt.QtCompat.translate("CustomDialog",  # context
                                   "Status",  # sourceText
                                   None,  # disambiguation
                                   -1)  # n
    assert result == u'Status', result


def test_binding_and_qt_version():
    """Qt's __binding_version__ and __qt_version__ populated"""

    import Qt

    assert Qt.__binding_version__ != "0.0.0", ("Binding version was not "
                                               "populated")
    assert Qt.__qt_version__ != "0.0.0", ("Qt version was not populated")


def test_binding_states():
    """Tests to see if the Qt binding enum states are set properly"""
    import Qt
    assert Qt.IsPySide == binding("PySide")
    assert Qt.IsPySide2 == binding("PySide2")
    assert Qt.IsPyQt5 == binding("PyQt5")
    assert Qt.IsPyQt4 == binding("PyQt4")


def test_qtcompat_base_class():
    """Tests to ensure the QtCompat namespace object works as expected"""
    import sys
    import Qt
    from Qt import QtWidgets
    from Qt import QtCompat
    app = QtWidgets.QApplication(sys.argv)
    # suppress `local variable 'app' is assigned to but never used`
    app
    header = QtWidgets.QHeaderView(Qt.QtCore.Qt.Horizontal)

    # Spot check compatibility functions
    QtCompat.QHeaderView.setSectionsMovable(header, False)
    assert QtCompat.QHeaderView.sectionsMovable(header) is False
    QtCompat.QHeaderView.setSectionsMovable(header, True)
    assert QtCompat.QHeaderView.sectionsMovable(header) is True


def test_cli():
    """Qt.py is available from the command-line"""
    env = os.environ.copy()
    env.pop("QT_VERBOSE")  # Do not include debug messages

    popen = subprocess.Popen(
        [sys.executable, "Qt.py", "--help"],
        stdout=subprocess.PIPE,
        env=env
    )

    out, err = popen.communicate()
    assert out.startswith(b"usage: Qt.py"), "\n%s" % out


def test_membership():
    """All members of Qt.py exist in all bindings"""
    import Qt

    missing = list()
    for module, members in Qt._common_members.items():
        missing.extend(
            member for member in members
            if not hasattr(getattr(Qt, module), member)
        )

    binding = Qt.__binding__
    assert not missing, (
        "Some members did not exist in {binding}\n{missing}".format(
            **locals())
    )


if sys.version_info <= (3, 4):
    # PySide is not available for Python > 3.4
    # Shiboken(1) doesn't support Python 3.5
    # https://github.com/PySide/shiboken-setup/issues/3

    def test_wrapInstance():
        """.wrapInstance and .getCppPointer is identical across all bindings"""
        from Qt import QtCompat, QtWidgets

        app = QtWidgets.QApplication(sys.argv)

        try:
            button = QtWidgets.QPushButton("Hello world")
            button.setObjectName("MySpecialButton")
            pointer = QtCompat.getCppPointer(button)
            widget = QtCompat.wrapInstance(long(pointer),
                                           QtWidgets.QWidget)
            assert isinstance(widget, QtWidgets.QWidget), widget
            assert widget.objectName() == button.objectName()

            # IMPORTANT: this differs across sip and shiboken.
            if binding("PySide") or binding("PySide2"):
                assert widget != button
            else:
                assert widget == button

        finally:
            app.exit()

    def test_implicit_wrapInstance():
        """.wrapInstance doesn't need the `base` argument"""
        from Qt import QtCompat, QtWidgets

        app = QtWidgets.QApplication(sys.argv)

        try:
            button = QtWidgets.QPushButton("Hello world")
            button.setObjectName("MySpecialButton")
            pointer = QtCompat.getCppPointer(button)
            widget = QtCompat.wrapInstance(long(pointer))
            assert isinstance(widget, QtWidgets.QWidget), widget
            assert widget.objectName() == button.objectName()

            if binding("PySide") or binding("PySide2"):
                assert widget != button
            else:
                assert widget == button

        finally:
            app.exit()


if binding("PyQt4"):
    def test_preferred_pyqt4():
        """QT_PREFERRED_BINDING = PyQt4 properly forces the binding"""
        import Qt
        assert Qt.__binding__ == "PyQt4", (
            "PyQt4 should have been picked, "
            "instead got %s" % Qt.__binding__)

    def test_sip_api_qtpy():
        """Preferred binding PyQt4 should have sip version 2"""

        __import__("Qt")  # Bypass linter warning
        import sip
        assert sip.getapi("QString") == 2, (
            "PyQt4 API version should be 2, "
            "instead is %s" % sip.getapi("QString"))

    if PYTHON == 2:
        def test_sip_api_already_set():
            """Raise ImportError with sip was set to 1 with no hint, default"""
            __import__("PyQt4.QtCore")  # Bypass linter warning
            import sip
            sip.setapi("QString", 1)
            assert_raises(ImportError, __import__, "Qt")

        # A sip API hint of any kind bypasses ImportError
        # on account of it being merely a hint.
        def test_sip_api_1_1():
            """sip=1, hint=1 == OK"""
            import sip
            sip.setapi("QString", 1)
            os.environ["QT_SIP_API_HINT"] = "1"
            __import__("Qt")  # Bypass linter warning

        def test_sip_api_2_1():
            """sip=2, hint=1 == WARNING"""
            import sip
            sip.setapi("QString", 2)
            os.environ["QT_SIP_API_HINT"] = "1"

            with captured_output() as out:
                __import__("Qt")  # Bypass linter warning
                stdout, stderr = out
                assert stderr.getvalue().startswith("Warning:")

        def test_sip_api_1_2():
            """sip=1, hint=2 == WARNING"""
            import sip
            sip.setapi("QString", 1)
            os.environ["QT_SIP_API_HINT"] = "2"

            with captured_output() as out:
                __import__("Qt")  # Bypass linter warning
                stdout, stderr = out
                assert stderr.getvalue().startswith("Warning:")

        def test_sip_api_2_2():
            """sip=2, hint=2 == OK"""
            import sip
            sip.setapi("QString", 2)
            os.environ["QT_SIP_API_HINT"] = "2"
            __import__("Qt")  # Bypass linter warning


if binding("PyQt5"):
    def test_preferred_pyqt5():
        """QT_PREFERRED_BINDING = PyQt5 properly forces the binding"""
        import Qt
        assert Qt.__binding__ == "PyQt5", (
            "PyQt5 should have been picked, "
            "instead got %s" % Qt.__binding__)


if binding("PySide"):
    def test_preferred_pyside():
        """QT_PREFERRED_BINDING = PySide properly forces the binding"""
        import Qt
        assert Qt.__binding__ == "PySide", (
            "PySide should have been picked, "
            "instead got %s" % Qt.__binding__)


if binding("PySide2"):
    def test_preferred_pyside2():
        """QT_PREFERRED_BINDING = PySide2 properly forces the binding"""
        import Qt
        assert Qt.__binding__ == "PySide2", (
            "PySide2 should have been picked, "
            "instead got %s" % Qt.__binding__)

    def test_coexistence():
        """Qt.py may be use alongside the actual binding"""

        from Qt import QtCore
        import PySide2.QtGui

        # Qt remaps QStringListModel
        assert QtCore.QStringListModel

        # But does not delete the original
        assert PySide2.QtGui.QStringListModel


if binding("PyQt4") or binding("PyQt5"):
    def test_multiple_preferred():
        """QT_PREFERRED_BINDING = more than one binding excludes others"""

        # PySide is the more desirable binding
        os.environ["QT_PREFERRED_BINDING"] = os.pathsep.join(
            ["PyQt4", "PyQt5"])

        import Qt
        assert Qt.__binding__ == "PyQt4", (
            "PyQt4 should have been picked, "
            "instead got %s" % Qt.__binding__)
