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


def test_sip_api_pyqt4():
    """PyQt4 default sip API version"""

    from PyQt4 import QtCore
    import sip
    if sys.version_info[0] == 2:
        # Python 2.x
        assert sip.getapi("QString") == 1, ("PyQt4 API version should be 1, "
                                            "instead is %s"
                                            % sip.getapi("QString"))
    elif sys.version_info[0] == 3:
        # Python 3.x
        assert sip.getapi("QString") == 2, ("PyQt4 API version should be 2, "
                                            "instead is %s"
                                            % sip.getapi("QString"))

def test_sip_api_qtpy():
    """Qt.py with preferred binding PyQt4 should have sip version 2"""

    with pyqt4():
        import Qt
        import sip
        assert sip.getapi("QString") == 2, ("PyQt4 API version should be 2, "
                                            "instead is %s"
                                            % sip.getapi("QString"))

def test_sip_api_already_set():
    """Qt.py should cause ImportError when sip API v1 was already set"""

    with pyqt4():
        def import_qt():
            import Qt

        if sys.version_info[0] == 2:
            # Python 2.x

            from PyQt4 import QtCore
            import sip
            sip.setapi("QString", 1)
            assert_raises(ImportError, import_qt)
