import sys
import os

# Set preferred binding, or Qt.py tests will fail which doesn't have pysideuic
os.environ['QT_PREFERRED_BINDING'] = 'PyQt4'

from Qt import QtWidgets, __binding__


def load_ui_type(uifile):
    """Pyside equivalent for the loadUiType function in PyQt.

    From the PyQt4 documentation:
        Load a Qt Designer .ui file and return a tuple of the generated form
        class and the Qt base class. These can then be used to create any
        number of instances of the user interface without having to parse the
        .ui file more than once.

    Note:
        Pyside lacks the "loadUiType" command, so we have to convert the ui
        file to py code in-memory first and then execute it in a special frame
        to retrieve the form_class.

    Args:
        uifile (str): Absolute path to .ui file


    Returns:
        tuple: the generated form class, the Qt base class
    """
    import pysideuic
    import xml.etree.ElementTree as ElementTree
    from cStringIO import StringIO

    parsed = ElementTree.parse(uifile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(uifile, 'r') as f:
        o = StringIO()
        frame = {}

        pysideuic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec(pyc) in frame

        # Fetch the base_class and form class based on their type in
        # the xml from designer
        form_class = frame['Ui_%s' % form_class]
        base_class = eval('QtWidgets.%s' % widget_class)
    return form_class, base_class


def pyside_load_ui(uifile, base_instance=None):
    """Provide PyQt4.uic.loadUi functionality to PySide

    Args:
        uifile (str): Absolute path to .ui file
        base_instance (QWidget): The widget into which UI widgets are loaded


    Note:
        pysideuic is required for this to work with PySide.

        This seems to work correctly in Maya as well as outside of it as
        opposed to other implementations which involve overriding QUiLoader.

    Returns:
        QWidget: the base instance

    """
    form_class, base_class = load_ui_type(uifile)
    if not base_instance:
        typeName = form_class.__name__
        finalType = type(typeName,
                         (form_class, base_class),
                         {})
        base_instance = finalType()
    else:
        if not isinstance(base_instance, base_class):
            raise RuntimeError(
                'The base_instance passed to loadUi does not inherit from'
                ' needed base type (%s)' % type(base_class))
        typeName = type(base_instance).__name__
        base_instance.__class__ = type(typeName,
                                       (form_class, type(base_instance)),
                                       {})
    base_instance.setupUi(base_instance)
    return base_instance


def load_ui_wrapper(uifile, base_instance=None):
    """Load a Qt Designer .ui file and returns an instance of the user interface

    Args:
        uifile (str): Absolute path to .ui file
        base_instance (QWidget): The widget into which UI widgets are loaded

    Returns:
        function: pyside_load_ui or uic.loadUi

    """
    if 'PySide' in __binding__:
        return pyside_load_ui(uifile, base_instance)
    elif 'PyQt' in __binding__:
        uic = __import__(__binding__ + ".uic").uic
        return uic.loadUi(uifile, base_instance)


class MainWindow(QtWidgets.QWidget):
    """Load .ui file example, utilizing pysideuic and/or PyQt4.uic.loadUi"""
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.base_instance = load_ui_wrapper('qwidget.ui', self)


def test():
    """Example: load_ui with custom uic.loadUi-like wrapper"""
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
