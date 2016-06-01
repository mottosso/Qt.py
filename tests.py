"""Nose tests

Usage:
    $ nosetests .

"""

import os
import sys
import imp

from nose.tools import (
    with_setup,
    assert_raises,
)


def _clean():
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


@with_setup(_clean)
def test_preferred():
    """Setting QT_PREFERRED_BINDING properly forces a particular binding"""
    sys.modules.pop("Qt", None)
    os.environ.pop("QT_PREFERRED_BINDING", None)

    import Qt

    # PySide is the more desirable binding
    assert Qt.__name__ != "PyQt4", ("PySide should have been picked, "
                                    "instead got %s" % Qt)

    # Try again
    sys.modules.pop("Qt")
    os.environ["QT_PREFERRED_BINDING"] = "PySide"

    import Qt
    assert Qt.__name__ == "PySide", ("PySide should have been picked, "
                                     "instead got %s" % Qt)


@with_setup(_clean)
def test_preferred_none():
    """Preferring None shouldn't import anything"""

    os.environ["QT_PREFERRED_BINDING"] = "None"
    import Qt
    assert Qt.__name__ == "Qt", Qt
