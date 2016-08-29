import sys
import os

# Set preferred binding
# os.environ["QT_PREFERRED_BINDING"] = "PySide"

from Qt import QtWidgets
from Qt import __binding__


def loadUiType(uiFile):
    """
    Pyside equiv for the loadUiType function in qt.
    """

    import pysideuic
    import xml.etree.ElementTree as ElementTree
    from cStringIO import StringIO

    parsed = ElementTree.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(uiFile, 'r') as f:
        o = StringIO()
        frame = {}

        pysideuic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        # Fetch the base_class and form class based on their type in
        # the xml from designer
        form_class = frame['Ui_%s' % form_class]
        base_class = eval('QtWidgets.%s' % widget_class)
    return form_class, base_class


def loadUi(uifile, baseinstance=None, workingDirectory=None):
    """
    An implementation that uses the custom loadUiType above.
    This seems to work correctly in Maya as well as outside of it as
    opposed to other implementation what overrride QUiLoader.
    """
    form_class, base_class = loadUiType(uifile)
    if not baseinstance:
        typeName = form_class.__name__
        finalType = type(typeName,
                         (form_class, base_class),
                         {})
        baseinstance = finalType()
    else:
        if not isinstance(baseinstance, base_class):
            raise RuntimeError(
                "The baseinstance passed to loadUi does not inherit from"
                " needed base type (%s)" % type(base_class))
        typeName = type(baseinstance).__name__
        baseinstance.__class__ = type(typeName,
                                      (form_class, type(baseinstance)),
                                      {})
    baseinstance.setupUi(baseinstance)
    return baseinstance


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        if 'PySide' in __binding__:
            loadUi('examples/load_ui_qwidget.ui', self)
        elif 'PyQt' in __binding__:
            from Qt import uic
            uic.loadUi('examples/load_ui_qwidget.ui', self)


def test_load_ui_setup_ui_wrapper():
    """Example: load_ui with custom loadUiType
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
