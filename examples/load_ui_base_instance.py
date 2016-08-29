import sys
import os

# Set preferred binding
os.environ["QT_PREFERRED_BINDING"] = "PySide:PyQt4"

from Qt import QtWidgets, load_ui


def setup_ui(uifile, base_instance=None):
    ui = load_ui(uifile)
    if not base_instance:
        return ui
    else:
        for member in dir(ui):
            if not member.startswith('__') and \
               member is not 'staticMetaObject':
                setattr(base_instance, member, getattr(ui, member))
        return ui


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        setup_ui('examples/load_ui_qwidget.ui', self)


def test_load_ui_setup_ui_wrapper():
    """Example: load_ui with setup_ui wrapper
    """
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()

    # Tests
    assert isinstance(window.__class__, QtWidgets.QWidget.__class__)
    assert isinstance(window.parent(), type(None))
    assert isinstance(window.lineEdit.__class__, QtWidgets.QWidget.__class__)
    assert window.lineEdit.text() == ''
    window.lineEdit.setText('Hello')
    assert window.lineEdit.text() == 'Hello'

    app.exit()
