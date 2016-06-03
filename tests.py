"""Nose tests

Usage:
    $ nosetests .

"""

import os
import sys
import imp
import contextlib

from nose.tools import (
    with_setup,
    assert_raises,
)


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


def clean():
    """Provide clean working environment"""
    sys.modules.pop("Qt", None)
    os.environ.pop("QT_PREFERRED_BINDING", None)


def test_environment():
    """Tests require PySide and PyQt4 bindings to be installed"""

    imp.find_module("PySide")
    imp.find_module("PyQt4")

    # These should *not* be available
    assert_raises(ImportError, imp.find_module, "PySide2")
    assert_raises(ImportError, imp.find_module, "PyQt5")


@with_setup(clean)
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


@with_setup(clean)
def test_preferred_none():
    """Preferring None shouldn't import anything"""

    os.environ["QT_PREFERRED_BINDING"] = "None"
    import Qt
    assert Qt.__name__ == "Qt", Qt


@with_setup(clean)
def test_coexistence():
    """Qt.py may be use alongside the actual binding"""

    with pyside():
        from Qt import QtCore
        import PySide.QtGui

        # Qt remaps QStringListModel
        assert QtCore.QStringListModel

        # But does not delete the original
        assert PySide.QtGui.QStringListModel


@with_setup(clean)
def test_sip_api_pyqt4():
    """PyQt should have sip version 1"""

    from PyQt4 import QtCore
    import sip
    api_version = sip.getapi("QString")
    assert api_version == 1, ("PyQt4 API version should be 1, "
                              "instead is %s" % api_version)


@with_setup(clean)
def test_sip_api_qtpy():
    """Qt.py with preferred binding PyQt4 should have sip version 2"""

    sys.modules.pop("sip")
    os.environ["QT_PREFERRED_BINDING"] = "PyQt4"
    import Qt
    import sip
    api_version = sip.getapi("QString")
    assert api_version == 2, ("PyQt4 API version should be 2, "
                              "instead is %s" % api_version)
