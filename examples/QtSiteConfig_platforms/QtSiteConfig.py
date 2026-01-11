import sys


IS_WIN = sys.platform == "win32"


def update_members(members):
    # Add windows only `QWinEventNotifier` class
    if IS_WIN:
        members["QtCore"].append("QWinEventNotifier")

        # Add the windows only QtAxContainer class. The PySideX bindings use
        # the QtAxContainer module name, so we can just add them here
        members["QtAxContainer"] = ["QAxBase", "QAxObject", "QAxWidget"]


def update_misplaced_members(members):
    if IS_WIN:
        # Correctly map the Windows only QtAxContainer misplaced in PyQtX.
        # PySide6/2 uses the QtAxContainer module name, rename PyQt's module.
        for bnd in ("PyQt6", "PyQt5"):
            # We have to add "QAxContainer" to __extras__ so it's imported
            # by Qt.py and available for misplaced_members to access
            members[bnd].setdefault("__extras__", []).append("QAxContainer")
            # Add each individual misplaced member mapping to add to Qt.py
            members[bnd]["QAxContainer.QAxBase"] = "QtAxContainer.QAxBase"
            members[bnd]["QAxContainer.QAxObject"] = "QtAxContainer.QAxObject"
            members[bnd]["QAxContainer.QAxWidget"] = "QtAxContainer.QAxWidget"
