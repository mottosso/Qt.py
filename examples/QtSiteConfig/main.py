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


if __name__ == '__main__':
    test()
