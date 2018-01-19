"""Example of QtSiteConfig module used to modify exposed members of Qt.py"""

import os
import sys


def test():
    """QtCore is taken out of Qt.py via QtSiteConfig.py"""

    # Expose this directory, and therefore QtSiteConfig, to Python
    sys.path.insert(0, os.path.dirname(__file__))

    try:
        from Qt import QtCore

    except ImportError:
        print("Qt.QtCore was successfully removed by QtSiteConfig.py")

    else:
        raise ImportError(
            "Qt.QtCore was importable, update_members was not "
            "applied correctly."
        )

        # Suppress "Qt.QtCore" imported but unused warning
        QtCore

    # Test _misplaced_members is applied correctly
    from Qt import QtGui
    assert QtGui.QColorTest == QtGui.QColor, (
        "QtGui.QColor was not mapped to QtGui.QColorTest"
    )

    # Test _compatibility_members is applied correctly
    title = "Test Widget"
    from Qt import QtWidgets, QtCompat
    app = QtWidgets.QApplication(sys.argv)
    wid = QtWidgets.QWidget()
    wid.setWindowTitle(title)

    # Verify that our simple remapping of QWidget.windowTitle works
    assert QtCompat.QWidget.windowTitleTest(wid) == title, (
        "Non-decorated function was added to QtCompat.QWidget"
    )
    # Verify that our decorated remapping of QWidget.windowTitle works
    check = "Test: {}".format(title)
    assert QtCompat.QWidget.windowTitleDecorator(wid) == check, (
        "Decorated method was not added to QtCompat.QWidget"
    )

    # Verify that our decorated remapping of QMainWindow.windowTitle is
    # different than the QWidget version.
    win = QtWidgets.QMainWindow()
    win.setWindowTitle(title)
    check = "QMainWindow Test: {}".format(title)
    assert QtCompat.QMainWindow.windowTitleDecorator(win) == check, (
        "Decorated method was added to QtCompat.QMainWindow"
    )
    # Suppress "app" imported but unused warning
    app


if __name__ == "__main__":
    test()
