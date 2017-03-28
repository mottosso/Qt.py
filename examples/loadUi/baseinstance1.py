import sys
import os

# Set preferred binding
os.environ['QT_PREFERRED_BINDING'] = os.pathsep.join(['PySide', 'PyQt4'])

from Qt import QtWidgets, QtCompat


def setup_ui(uifile, base_instance=None):
    """Load a Qt Designer .ui file and returns an instance of the user interface

    Args:
        uifile (str): Absolute path to .ui file
        base_instance (QWidget): The widget into which UI widgets are loaded

    Returns:
        QWidget: the base instance

    """
    ui = QtCompat.loadUi(uifile)  # Qt.py mapped function
    if not base_instance:
        return ui
    else:
        for member in dir(ui):
            if not member.startswith('__') and \
               member is not 'staticMetaObject':
                setattr(base_instance, member, getattr(ui, member))
        return ui


class MainWindow(QtWidgets.QWidget):
    """Load .ui file example, using setattr/getattr approach"""
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.base_instance = setup_ui('qwidget.ui', self)


def test():
    """Example: QtCompat.loadUi with setup_ui wrapper"""
    working_directory = os.path.dirname(__file__)
    os.chdir(working_directory)

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()

    # Tests
    assert isinstance(window, QtWidgets.QWidget)
    assert isinstance(window.parent(), type(None))
    assert isinstance(window.base_instance, QtWidgets.QWidget)
    assert isinstance(window.lineEdit, QtWidgets.QWidget)
    assert window.lineEdit.text() == ''
    window.lineEdit.setText('Hello')
    assert window.lineEdit.text() == 'Hello'

    app.exit()
