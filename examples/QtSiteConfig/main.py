"""Example of QtSideConfig module used to modify exposed members of Qt.py"""

import os
import sys


def test():
    """QtCore is taken out of Qt.py via QSiteConfig.py"""

    # Expose this directory, and therefore QtSiteConfig, to Python
    sys.path.insert(0, os.path.dirname(__file__))

    try:
        from Qt import QtCore

    except ImportError:
        print("Qt.QtCore was successfully removed by QSideConfig.py")

    else:
        raise ImportError(
            "Qt.QtCore was importable, update_members was not "
            "applied correctly."
        )

        # Suppress 'Qt.QtCore' imported but unused warning
        QtCore

    # Test _compatibility_members is applied correctly
    title = 'Test Widget'
    from Qt import QtWidgets, QtCompat
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QWidget()
    win.setWindowTitle(title)

    # Verify that our simple remapping of QWidget.windowTitle works
    assert QtCompat.QWidget.windowTitleTest(win) == title
    # Verify that our decorated remapping of QWidget.windowTitle works
    check = 'Test: {}'.format(title)
    assert QtCompat.QWidget.windowTitleDecorator(win) == check


if __name__ == '__main__':
    test()
