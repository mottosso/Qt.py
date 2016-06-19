"""Nose tests

Usage:
    $ nosetests .

"""

import os
import sys
import imp
import shutil
import tempfile
import subprocess
import contextlib

from nose.tools import (
    with_setup,
    assert_raises,
)

PYTHON = sys.version_info[0]  # e.g. 2 or 3


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
        import Qt
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

    dirname = os.path.dirname(__file__)
    tempdir = tempfile.mkdtemp()

    try:
        project = os.path.join(tempdir, "myproject")
        vendor = os.path.join(tempdir, "myproject", "vendor")

        os.makedirs(vendor)

        # Make packages out of folders
        with open(os.path.join(project, "__init__.py"), "w") as f:
            f.write("from .vendor.Qt import QtWidgets")

        with open(os.path.join(vendor, "__init__.py"), "w") as f:
            pass

        shutil.copy(os.path.join(dirname, "Qt.py"),
                    os.path.join(vendor, "Qt.py"))

        print("Testing relative import..")
        assert subprocess.call(
            ["python", "-c", "import myproject"],
            cwd=tempdir,
            env={}
        ) == 0

        print("Testing absolute import..")
        assert subprocess.call(
            ["python", "-c", "from myproject.vendor.Qt import QtWidgets"],
            cwd=tempdir,
            env={}
        ) == 0

        print("Testing direct import..")
        assert subprocess.call(
            ["python", "-c", "import myproject.vendor.Qt"],
            cwd=tempdir,
            env={}
        ) == 0

    finally:
        shutil.rmtree(tempdir)


if PYTHON == 2:
    def test_sip_api_already_set():
        """Raise ImportError if sip API v1 was already set (Python 2.x only)"""

        with pyqt4():
            from PyQt4 import QtCore
            import sip
            sip.setapi("QString", 1)
            assert_raises(ImportError, __import__, "Qt")
