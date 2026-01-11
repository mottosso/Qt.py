"""Example of QtSiteConfig module used to modify exposed members of Qt.py"""

import os
import sys

IS_WIN = sys.platform == "win32"
print(f'Platform {"is" if IS_WIN else "is not"} windows: "{sys.platform}"')


def test():
    """QtCore is taken out of Qt.py via QtSiteConfig.py"""

    # Expose this directory, and therefore QtSiteConfig, to Python
    sys.path.insert(0, os.path.dirname(__file__))

    try:
        from Qt.QtCore import QWinEventNotifier  # noqa: F401
    except ImportError:
        if IS_WIN:
            raise ImportError(
                "Qt.QtCore.QWinEventNotifier is not importable on windows"
                "update_members was not applied correctly."
            ) from None
        else:
            print(
                "Qt.QtCore.QWinEventNotifier was not added on this non-windows platform"
            )
    else:
        if IS_WIN:
            print(
                "Qt.QtCore.QWinEventNotifier was added on windows via QtSiteConfig.py"
            )
        else:
            raise ImportError(
                "Qt.QtCore.QWinEventNotifier was importable, on this "
                "non-windows platform. This should be impossible."
            ) from None

    # Test _misplaced_members is applied correctly
    import Qt

    assert not hasattr(Qt, "QAxContainer")
    if IS_WIN:
        assert Qt.QtAxContainer
        assert Qt.QtAxContainer.QAxBase
        assert Qt.QtAxContainer.QAxWidget
        print("Qt.QtAxContainer and members were added on windows.")
    else:
        assert not hasattr(Qt, "QtAxContainer")
        print("Qt.QtAxContainer and members was not added on non-windows.")


if __name__ == "__main__":
    test()
