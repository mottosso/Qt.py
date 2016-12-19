"""The MIT License (MIT)

Copyright (c) 2016-2017 Marcus Ottosson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Documentation

    All members of PySide2 are mapped from other bindings, should they exist.
    If no equivalent member exist, it is excluded from Qt.py and inaccessible.
    The idea is to highlight members that exist across all supported binding,
    and guarantee that code that runs on one binding runs on all others.

    For more details, visit https://github.com/mottosso/Qt.py

"""

import os
import sys
import types
import shutil

# Flags from environment variables
QT_VERBOSE = bool(os.getenv("QT_VERBOSE"))                # Extra output
QT_TESTING = bool(os.getenv("QT_TESTING"))                # Extra constraints
QT_PREFERRED_BINDING = os.getenv("QT_PREFERRED_BINDING")  # Override default

# Supported submodules
Qt = types.ModuleType("Qt")
QtGui = types.ModuleType("QtGui")
QtCore = types.ModuleType("QtCore")
QtWidgets = types.ModuleType("QtWidgets")
QtCompat = types.ModuleType("QtCompat")

# Enable direct import of submodules
# E.g. import Qt.QtCore
sys.modules.update({
    __name__ + ".QtGui": QtGui,
    __name__ + ".QtCore": QtCore,
    __name__ + ".QtWidgets": QtWidgets,
    __name__ + ".QtCompat": QtCompat,
})


def _remap(object, name, value, safe=True):
    """Prevent accidental assignment of existing members

    Arguments:
        object (object): Parent of new attribute
        name (str): Name of new attribute
        value (object): Value of new attribute
        safe (bool): Whether or not to guarantee that
            the new attribute was not overwritten.
            Can be set to False under condition that
            it is superseded by extensive testing.

    """

    if QT_TESTING and safe:
        # Cannot alter original binding.
        if hasattr(object, name):
            raise AttributeError("Cannot override existing name: "
                                 "%s.%s" % (object.__name__, name))

        # Cannot alter classes of functions
        if type(object).__name__ != "module":
            raise AttributeError("%s != 'module': Cannot alter "
                                 "anything but modules" % object)

    elif hasattr(object, name):
        # Keep track of modifications
        QtCompat.__modified__.append(name)

    QtCompat.__remapped__.append(name)

    setattr(object, name, value)


def _add(object, name, value):
    """Append to self, accessible via Qt.QtCompat"""
    QtCompat.__added__.append(name)
    setattr(object, name, value)


def _pyside2():
    from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools, __version__

    QtCompat.__binding__ = "PySide2"
    QtCompat.__qt_version__ = QtCore.qVersion()
    QtCompat.__binding_version__ = __version__
    QtCompat.load_ui = lambda fname: QtUiTools.QUiLoader().load(fname)
    QtCompat.setSectionResizeMode = QtWidgets.QHeaderView.setSectionResizeMode
    QtCompat.translate = QtCore.QCoreApplication.translate

    return QtCore, QtGui, QtWidgets


def _pyside():
    from PySide import QtGui, QtCore, QtUiTools, __version__

    QtWidgets = QtGui

    QtCompat.__binding__ = "PySide"
    QtCompat.__qt_version__ = QtCore.qVersion()
    QtCompat.__binding_version__ = __version__
    QtCompat.load_ui = lambda fname: QtUiTools.QUiLoader().load(fname)
    QtCompat.setSectionResizeMode = QtGui.QHeaderView.setResizeMode
    QtCompat.translate = (
        lambda context, sourceText, disambiguation, n:
        QtCore.QCoreApplication.translate(context,
                                          sourceText,
                                          disambiguation,
                                          QtCore.QCoreApplication.CodecForTr,
                                          n))
    return QtCore, QtGui, QtWidgets


def _pyqt5():
    from PyQt5 import QtWidgets, QtGui, QtCore, uic

    QtCompat.__binding__ = "PyQt5"
    QtCompat.__qt_version__ = QtCore.QT_VERSION_STR
    QtCompat.__binding_version__ = QtCore.PYQT_VERSION_STR
    QtCompat.load_ui = lambda fname: uic.loadUi(fname)
    QtCompat.translate = QtCore.QCoreApplication.translate
    QtCompat.setSectionResizeMode = QtWidgets.QHeaderView.setSectionResizeMode

    return QtCore, QtGui, QtWidgets


def _pyqt4():
    import sip
    try:
        sip.setapi("QString", 2)
        sip.setapi("QVariant", 2)
        sip.setapi("QDate", 2)
        sip.setapi("QDateTime", 2)
        sip.setapi("QTextStream", 2)
        sip.setapi("QTime", 2)
        sip.setapi("QUrl", 2)
    except AttributeError:
        raise ImportError
        # PyQt4 < v4.6
    except ValueError:
        # API version already set to v1
        raise ImportError

    from PyQt4 import QtGui, QtCore, uic

    QtWidgets = QtGui

    QtCompat.__binding__ = "PyQt4"
    QtCompat.__qt_version__ = QtCore.QT_VERSION_STR
    QtCompat.__binding_version__ = QtCore.PYQT_VERSION_STR
    QtCompat.load_ui = lambda fname: uic.loadUi(fname)
    QtCompat.setSectionResizeMode = QtGui.QHeaderView.setResizeMode

    # PySide2 differs from Qt4 in that Qt4 has one extra argument
    # which is always `None`. The lambda arguments represents the PySide2
    # interface, whereas the arguments passed to `.translate` represent
    # those expected of a Qt4 binding.
    QtCompat.translate = (
        lambda context, sourceText, disambiguation, n:
        QtCore.QCoreApplication.translate(context,
                                          sourceText,
                                          disambiguation,
                                          QtCore.QCoreApplication.CodecForTr,
                                          n))

    return QtCore, QtGui, QtWidgets


def _none():
    """Internal option (used in installer)"""

    Mock = type("Mock", (), {"__getattr__": lambda self, attr: None})

    QtCompat.__binding__ = "None"
    QtCompat.__qt_version__ = "0.0.0"
    QtCompat.__binding_version__ = "0.0.0"
    QtCompat.load_ui = lambda fname: None
    QtCompat.setSectionResizeMode = lambda *args, **kwargs: None

    return Mock(), Mock(), Mock()


def _log(text):
    if QT_VERBOSE:
        sys.stdout.write(text + "\n")


# Default order (customise order and content via QT_PREFERRED_BINDING)
_bindings = (_pyside2, _pyqt5, _pyside, _pyqt4)

if QT_PREFERRED_BINDING:
    _preferred = QT_PREFERRED_BINDING.split(os.pathsep)
    _available = {
        "PySide2": _pyside2,
        "PyQt5": _pyqt5,
        "PySide": _pyside,
        "PyQt4": _pyqt4,
        "None": _none
    }

    try:
        _bindings = [_available[binding] for binding in _preferred]
    except KeyError:
        raise ImportError(
            ("Requested %s, available: " % _preferred) +
            "\n".join(_available.keys())
        )

    del(_preferred)
    del(_available)

_log("Preferred binding: %s" % list(_b.__name__ for _b in _bindings))


_found_finding = False
for _binding in _bindings:
    _log("Trying %s" % _binding.__name__)

    try:
        _QtCore, _QtGui, _QtWidgets = _binding()
        _found_finding = True
        break

    except ImportError as e:
        _log("ImportError(\"%s\")" % e)
        continue

if not _found_finding:
    # If not binding were found, throw this error
    raise ImportError("No Qt binding were found.")


def convert(lines):
    """Convert compiled .ui file from PySide2 to Qt.py

    Arguments:
        lines (list): Each line of of .ui file

    Usage:
        >> with open("myui.py") as f:
        ..   lines = convert(f.readlines())

    """

    def parse(line):
        line = line.replace("from PySide2 import", "from Qt import")
        line = line.replace("QtWidgets.QApplication.translate",
                            "Qt.QtCompat.translate")
        return line

    parsed = list()
    for line in lines:
        line = parse(line)
        parsed.append(line)

    return parsed


def _cli(args):
    """Qt.py command-line interface"""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--convert",
                        help="Path to compiled Python module, e.g. my_ui.py")
    parser.add_argument("--compile",
                        help="Accept raw .ui file and compile with native "
                             "PySide2 compiler.")
    parser.add_argument("--stdout",
                        help="Write to stdout instead of file",
                        action="store_true")
    parser.add_argument("--stdin",
                        help="Read from stdin instead of file",
                        action="store_true")

    args = parser.parse_args(args)

    if args.stdout:
        raise NotImplementedError("--stdout")

    if args.stdin:
        raise NotImplementedError("--stdin")

    if args.compile:
        raise NotImplementedError("--compile")

    if args.convert:
        sys.stdout.write("#\n"
                         "# WARNING: --convert is an ALPHA feature.\n#\n"
                         "# See https://github.com/mottosso/Qt.py/pull/132\n"
                         "# for details.\n"
                         "#\n")

        #
        # ------> Read
        #
        with open(args.convert) as f:
            lines = convert(f.readlines())

        backup = "%s_backup%s" % os.path.splitext(args.convert)
        sys.stdout.write("Creating \"%s\"..\n" % backup)
        shutil.copy(args.convert, backup)

        #
        # <------ Write
        #
        with open(args.convert, "w") as f:
            f.write("".join(lines))

        sys.stdout.write("Successfully converted \"%s\"\n" % args.convert)


QtCompat.__added__ = list()     # All members added to QtCompat
QtCompat.__remapped__ = list()  # Members copied from elsewhere
QtCompat.__modified__ = list()  # Existing members modified in some way
QtCompat.__version__ = "0.7.0"
QtCompat._remap = _remap
QtCompat._add = _add
QtCompat.cli = _cli

QtGui.QAbstractTextDocumentLayout = _QtGui.QAbstractTextDocumentLayout
# QtGui.QAccessibleEvent = _QtGui.QAccessibleEvent  # Not in PyQt4
QtGui.QActionEvent = _QtGui.QActionEvent
QtGui.QBitmap = _QtGui.QBitmap
QtGui.QBrush = _QtGui.QBrush
QtGui.QClipboard = _QtGui.QClipboard
QtGui.QCloseEvent = _QtGui.QCloseEvent
QtGui.QColor = _QtGui.QColor
QtGui.QConicalGradient = _QtGui.QConicalGradient
QtGui.QContextMenuEvent = _QtGui.QContextMenuEvent
QtGui.QCursor = _QtGui.QCursor
QtGui.QDoubleValidator = _QtGui.QDoubleValidator
QtGui.QDrag = _QtGui.QDrag
QtGui.QDragEnterEvent = _QtGui.QDragEnterEvent
QtGui.QDragLeaveEvent = _QtGui.QDragLeaveEvent
QtGui.QDragMoveEvent = _QtGui.QDragMoveEvent
QtGui.QDropEvent = _QtGui.QDropEvent
QtGui.QFileOpenEvent = _QtGui.QFileOpenEvent
QtGui.QFocusEvent = _QtGui.QFocusEvent
QtGui.QFont = _QtGui.QFont
QtGui.QFontDatabase = _QtGui.QFontDatabase
QtGui.QFontInfo = _QtGui.QFontInfo
QtGui.QFontMetrics = _QtGui.QFontMetrics
QtGui.QFontMetricsF = _QtGui.QFontMetricsF
QtGui.QGradient = _QtGui.QGradient
# QtGui.QGuiApplication = _QtGui.QGuiApplication
QtGui.QHelpEvent = _QtGui.QHelpEvent
QtGui.QHideEvent = _QtGui.QHideEvent
QtGui.QHoverEvent = _QtGui.QHoverEvent
QtGui.QIcon = _QtGui.QIcon
QtGui.QIconDragEvent = _QtGui.QIconDragEvent
QtGui.QIconEngine = _QtGui.QIconEngine
QtGui.QImage = _QtGui.QImage
QtGui.QImageIOHandler = _QtGui.QImageIOHandler
QtGui.QImageReader = _QtGui.QImageReader
QtGui.QImageWriter = _QtGui.QImageWriter
QtGui.QInputEvent = _QtGui.QInputEvent
QtGui.QInputMethodEvent = _QtGui.QInputMethodEvent
QtGui.QIntValidator = _QtGui.QIntValidator
QtGui.QKeyEvent = _QtGui.QKeyEvent
QtGui.QKeySequence = _QtGui.QKeySequence
QtGui.QLinearGradient = _QtGui.QLinearGradient
# QtGui.QMatrix = _QtGui.QMatrix  # Not in PyQt5
QtGui.QMatrix2x2 = _QtGui.QMatrix2x2
QtGui.QMatrix2x3 = _QtGui.QMatrix2x3
QtGui.QMatrix2x4 = _QtGui.QMatrix2x4
QtGui.QMatrix3x2 = _QtGui.QMatrix3x2
QtGui.QMatrix3x3 = _QtGui.QMatrix3x3
QtGui.QMatrix3x4 = _QtGui.QMatrix3x4
QtGui.QMatrix4x2 = _QtGui.QMatrix4x2
QtGui.QMatrix4x3 = _QtGui.QMatrix4x3
QtGui.QMatrix4x4 = _QtGui.QMatrix4x4
QtGui.QMouseEvent = _QtGui.QMouseEvent
QtGui.QMoveEvent = _QtGui.QMoveEvent
QtGui.QMovie = _QtGui.QMovie
# QtGui.QPagedPaintDevice = _QtGui.QPagedPaintDevice
QtGui.QPaintDevice = _QtGui.QPaintDevice
QtGui.QPaintEngine = _QtGui.QPaintEngine
QtGui.QPaintEngineState = _QtGui.QPaintEngineState
QtGui.QPaintEvent = _QtGui.QPaintEvent
QtGui.QPainter = _QtGui.QPainter
QtGui.QPainterPath = _QtGui.QPainterPath
QtGui.QPainterPathStroker = _QtGui.QPainterPathStroker
QtGui.QPalette = _QtGui.QPalette
QtGui.QPen = _QtGui.QPen
QtGui.QPicture = _QtGui.QPicture
QtGui.QPictureIO = _QtGui.QPictureIO
QtGui.QPixmap = _QtGui.QPixmap
QtGui.QPixmapCache = _QtGui.QPixmapCache
QtGui.QPolygon = _QtGui.QPolygon
QtGui.QPolygonF = _QtGui.QPolygonF
# QtGui.QPyTextObject = _QtGui.QPyTextObject  # Not in PyQt5
QtGui.QQuaternion = _QtGui.QQuaternion
QtGui.QRadialGradient = _QtGui.QRadialGradient
QtGui.QRegExpValidator = _QtGui.QRegExpValidator
QtGui.QRegion = _QtGui.QRegion
QtGui.QResizeEvent = _QtGui.QResizeEvent
QtGui.QSessionManager = _QtGui.QSessionManager
QtGui.QShortcutEvent = _QtGui.QShortcutEvent
QtGui.QShowEvent = _QtGui.QShowEvent
QtGui.QStandardItem = _QtGui.QStandardItem
QtGui.QStandardItemModel = _QtGui.QStandardItemModel
QtGui.QStatusTipEvent = _QtGui.QStatusTipEvent
# QtGui.QSurface = _QtGui.QSurface
# QtGui.QSurfaceFormat = _QtGui.QSurfaceFormat
QtGui.QSyntaxHighlighter = _QtGui.QSyntaxHighlighter
QtGui.QTabletEvent = _QtGui.QTabletEvent
QtGui.QTextBlock = _QtGui.QTextBlock
QtGui.QTextBlockFormat = _QtGui.QTextBlockFormat
QtGui.QTextBlockGroup = _QtGui.QTextBlockGroup
QtGui.QTextBlockUserData = _QtGui.QTextBlockUserData
QtGui.QTextCharFormat = _QtGui.QTextCharFormat
QtGui.QTextCursor = _QtGui.QTextCursor
QtGui.QTextDocument = _QtGui.QTextDocument
QtGui.QTextDocumentFragment = _QtGui.QTextDocumentFragment
QtGui.QTextFormat = _QtGui.QTextFormat
QtGui.QTextFragment = _QtGui.QTextFragment
QtGui.QTextFrame = _QtGui.QTextFrame
QtGui.QTextFrameFormat = _QtGui.QTextFrameFormat
QtGui.QTextImageFormat = _QtGui.QTextImageFormat
QtGui.QTextInlineObject = _QtGui.QTextInlineObject
QtGui.QTextItem = _QtGui.QTextItem
QtGui.QTextLayout = _QtGui.QTextLayout
QtGui.QTextLength = _QtGui.QTextLength
QtGui.QTextLine = _QtGui.QTextLine
QtGui.QTextList = _QtGui.QTextList
QtGui.QTextListFormat = _QtGui.QTextListFormat
QtGui.QTextObject = _QtGui.QTextObject
QtGui.QTextObjectInterface = _QtGui.QTextObjectInterface
QtGui.QTextOption = _QtGui.QTextOption
QtGui.QTextTable = _QtGui.QTextTable
QtGui.QTextTableCell = _QtGui.QTextTableCell
QtGui.QTextTableCellFormat = _QtGui.QTextTableCellFormat
QtGui.QTextTableFormat = _QtGui.QTextTableFormat
# QtGui.QToolBarChangeEvent = _QtGui.QToolBarChangeEvent  # Not in PyQt4
# QtGui.QTouchDevice = _QtGui.QTouchDevice
# QtGui.QTouchEvent = _QtGui.QTouchEvent
QtGui.QTransform = _QtGui.QTransform
QtGui.QValidator = _QtGui.QValidator
QtGui.QVector2D = _QtGui.QVector2D
QtGui.QVector3D = _QtGui.QVector3D
QtGui.QVector4D = _QtGui.QVector4D
QtGui.QWhatsThisClickedEvent = _QtGui.QWhatsThisClickedEvent
QtGui.QWheelEvent = _QtGui.QWheelEvent
# QtGui.QWindow = _QtGui.QWindow
QtGui.QWindowStateChangeEvent = _QtGui.QWindowStateChangeEvent
QtGui.qAlpha = _QtGui.qAlpha
QtGui.qBlue = _QtGui.qBlue
QtGui.qGray = _QtGui.qGray
QtGui.qGreen = _QtGui.qGreen
QtGui.qIsGray = _QtGui.qIsGray
QtGui.qRed = _QtGui.qRed
QtGui.qRgb = _QtGui.qRgb
QtGui.qRgb = _QtGui.qRgb


QtWidgets.QAbstractButton = _QtWidgets.QAbstractButton
QtWidgets.QAbstractGraphicsShapeItem = _QtWidgets.QAbstractGraphicsShapeItem
QtWidgets.QAbstractItemDelegate = _QtWidgets.QAbstractItemDelegate
QtWidgets.QAbstractItemView = _QtWidgets.QAbstractItemView
QtWidgets.QAbstractScrollArea = _QtWidgets.QAbstractScrollArea
QtWidgets.QAbstractSlider = _QtWidgets.QAbstractSlider
QtWidgets.QAbstractSpinBox = _QtWidgets.QAbstractSpinBox
QtWidgets.QAction = _QtWidgets.QAction
QtWidgets.QActionGroup = _QtWidgets.QActionGroup
QtWidgets.QApplication = _QtWidgets.QApplication
QtWidgets.QBoxLayout = _QtWidgets.QBoxLayout
QtWidgets.QButtonGroup = _QtWidgets.QButtonGroup
QtWidgets.QCalendarWidget = _QtWidgets.QCalendarWidget
QtWidgets.QCheckBox = _QtWidgets.QCheckBox
QtWidgets.QColorDialog = _QtWidgets.QColorDialog
QtWidgets.QColumnView = _QtWidgets.QColumnView
QtWidgets.QComboBox = _QtWidgets.QComboBox
QtWidgets.QCommandLinkButton = _QtWidgets.QCommandLinkButton
QtWidgets.QCommonStyle = _QtWidgets.QCommonStyle
QtWidgets.QCompleter = _QtWidgets.QCompleter
QtWidgets.QDataWidgetMapper = _QtWidgets.QDataWidgetMapper
QtWidgets.QDateEdit = _QtWidgets.QDateEdit
QtWidgets.QDateTimeEdit = _QtWidgets.QDateTimeEdit
QtWidgets.QDesktopWidget = _QtWidgets.QDesktopWidget
QtWidgets.QDial = _QtWidgets.QDial
QtWidgets.QDialog = _QtWidgets.QDialog
QtWidgets.QDialogButtonBox = _QtWidgets.QDialogButtonBox
QtWidgets.QDirModel = _QtWidgets.QDirModel
QtWidgets.QDockWidget = _QtWidgets.QDockWidget
QtWidgets.QDoubleSpinBox = _QtWidgets.QDoubleSpinBox
QtWidgets.QErrorMessage = _QtWidgets.QErrorMessage
QtWidgets.QFileDialog = _QtWidgets.QFileDialog
QtWidgets.QFileIconProvider = _QtWidgets.QFileIconProvider
QtWidgets.QFileSystemModel = _QtWidgets.QFileSystemModel
QtWidgets.QFocusFrame = _QtWidgets.QFocusFrame
QtWidgets.QFontComboBox = _QtWidgets.QFontComboBox
QtWidgets.QFontDialog = _QtWidgets.QFontDialog
QtWidgets.QFormLayout = _QtWidgets.QFormLayout
QtWidgets.QFrame = _QtWidgets.QFrame
QtWidgets.QGesture = _QtWidgets.QGesture
QtWidgets.QGestureEvent = _QtWidgets.QGestureEvent
QtWidgets.QGestureRecognizer = _QtWidgets.QGestureRecognizer
QtWidgets.QGraphicsAnchor = _QtWidgets.QGraphicsAnchor
QtWidgets.QGraphicsAnchorLayout = _QtWidgets.QGraphicsAnchorLayout
QtWidgets.QGraphicsBlurEffect = _QtWidgets.QGraphicsBlurEffect
QtWidgets.QGraphicsColorizeEffect = _QtWidgets.QGraphicsColorizeEffect
QtWidgets.QGraphicsDropShadowEffect = _QtWidgets.QGraphicsDropShadowEffect
QtWidgets.QGraphicsEffect = _QtWidgets.QGraphicsEffect
QtWidgets.QGraphicsEllipseItem = _QtWidgets.QGraphicsEllipseItem
QtWidgets.QGraphicsGridLayout = _QtWidgets.QGraphicsGridLayout
QtWidgets.QGraphicsItem = _QtWidgets.QGraphicsItem
# QtWidgets.QGraphicsItemAnimation = _QtWidgets.QGraphicsItemAnimation  # Not in PyQt4
QtWidgets.QGraphicsItemGroup = _QtWidgets.QGraphicsItemGroup
QtWidgets.QGraphicsLayout = _QtWidgets.QGraphicsLayout
QtWidgets.QGraphicsLayoutItem = _QtWidgets.QGraphicsLayoutItem
QtWidgets.QGraphicsLineItem = _QtWidgets.QGraphicsLineItem
QtWidgets.QGraphicsLinearLayout = _QtWidgets.QGraphicsLinearLayout
QtWidgets.QGraphicsObject = _QtWidgets.QGraphicsObject
QtWidgets.QGraphicsOpacityEffect = _QtWidgets.QGraphicsOpacityEffect
QtWidgets.QGraphicsPathItem = _QtWidgets.QGraphicsPathItem
QtWidgets.QGraphicsPixmapItem = _QtWidgets.QGraphicsPixmapItem
QtWidgets.QGraphicsPolygonItem = _QtWidgets.QGraphicsPolygonItem
QtWidgets.QGraphicsProxyWidget = _QtWidgets.QGraphicsProxyWidget
QtWidgets.QGraphicsRectItem = _QtWidgets.QGraphicsRectItem
QtWidgets.QGraphicsRotation = _QtWidgets.QGraphicsRotation
QtWidgets.QGraphicsScale = _QtWidgets.QGraphicsScale
QtWidgets.QGraphicsScene = _QtWidgets.QGraphicsScene
QtWidgets.QGraphicsSceneContextMenuEvent = _QtWidgets.QGraphicsSceneContextMenuEvent
QtWidgets.QGraphicsSceneDragDropEvent = _QtWidgets.QGraphicsSceneDragDropEvent
QtWidgets.QGraphicsSceneEvent = _QtWidgets.QGraphicsSceneEvent
QtWidgets.QGraphicsSceneHelpEvent = _QtWidgets.QGraphicsSceneHelpEvent
QtWidgets.QGraphicsSceneHoverEvent = _QtWidgets.QGraphicsSceneHoverEvent
QtWidgets.QGraphicsSceneMouseEvent = _QtWidgets.QGraphicsSceneMouseEvent
QtWidgets.QGraphicsSceneMoveEvent = _QtWidgets.QGraphicsSceneMoveEvent
QtWidgets.QGraphicsSceneResizeEvent = _QtWidgets.QGraphicsSceneResizeEvent
QtWidgets.QGraphicsSceneWheelEvent = _QtWidgets.QGraphicsSceneWheelEvent
QtWidgets.QGraphicsSimpleTextItem = _QtWidgets.QGraphicsSimpleTextItem
QtWidgets.QGraphicsTextItem = _QtWidgets.QGraphicsTextItem
QtWidgets.QGraphicsTransform = _QtWidgets.QGraphicsTransform
QtWidgets.QGraphicsView = _QtWidgets.QGraphicsView
QtWidgets.QGraphicsWidget = _QtWidgets.QGraphicsWidget
QtWidgets.QGridLayout = _QtWidgets.QGridLayout
QtWidgets.QGroupBox = _QtWidgets.QGroupBox
QtWidgets.QHBoxLayout = _QtWidgets.QHBoxLayout
QtWidgets.QHeaderView = _QtWidgets.QHeaderView
QtWidgets.QInputDialog = _QtWidgets.QInputDialog
QtWidgets.QItemDelegate = _QtWidgets.QItemDelegate
QtWidgets.QItemEditorCreatorBase = _QtWidgets.QItemEditorCreatorBase
QtWidgets.QItemEditorFactory = _QtWidgets.QItemEditorFactory
QtWidgets.QKeyEventTransition = _QtWidgets.QKeyEventTransition
QtWidgets.QLCDNumber = _QtWidgets.QLCDNumber
QtWidgets.QLabel = _QtWidgets.QLabel
QtWidgets.QLayout = _QtWidgets.QLayout
QtWidgets.QLayoutItem = _QtWidgets.QLayoutItem
QtWidgets.QLineEdit = _QtWidgets.QLineEdit
QtWidgets.QListView = _QtWidgets.QListView
QtWidgets.QListWidget = _QtWidgets.QListWidget
QtWidgets.QListWidgetItem = _QtWidgets.QListWidgetItem
QtWidgets.QMainWindow = _QtWidgets.QMainWindow
QtWidgets.QMdiArea = _QtWidgets.QMdiArea
QtWidgets.QMdiSubWindow = _QtWidgets.QMdiSubWindow
QtWidgets.QMenu = _QtWidgets.QMenu
QtWidgets.QMenuBar = _QtWidgets.QMenuBar
QtWidgets.QMessageBox = _QtWidgets.QMessageBox
QtWidgets.QMouseEventTransition = _QtWidgets.QMouseEventTransition
QtWidgets.QPanGesture = _QtWidgets.QPanGesture
QtWidgets.QPinchGesture = _QtWidgets.QPinchGesture
QtWidgets.QPlainTextDocumentLayout = _QtWidgets.QPlainTextDocumentLayout
QtWidgets.QPlainTextEdit = _QtWidgets.QPlainTextEdit
QtWidgets.QProgressBar = _QtWidgets.QProgressBar
QtWidgets.QProgressDialog = _QtWidgets.QProgressDialog
QtWidgets.QPushButton = _QtWidgets.QPushButton
QtWidgets.QRadioButton = _QtWidgets.QRadioButton
QtWidgets.QRubberBand = _QtWidgets.QRubberBand
QtWidgets.QScrollArea = _QtWidgets.QScrollArea
QtWidgets.QScrollBar = _QtWidgets.QScrollBar
QtWidgets.QShortcut = _QtWidgets.QShortcut
QtWidgets.QSizeGrip = _QtWidgets.QSizeGrip
QtWidgets.QSizePolicy = _QtWidgets.QSizePolicy
QtWidgets.QSlider = _QtWidgets.QSlider
QtWidgets.QSpacerItem = _QtWidgets.QSpacerItem
QtWidgets.QSpinBox = _QtWidgets.QSpinBox
QtWidgets.QSplashScreen = _QtWidgets.QSplashScreen
QtWidgets.QSplitter = _QtWidgets.QSplitter
QtWidgets.QSplitterHandle = _QtWidgets.QSplitterHandle
QtWidgets.QStackedLayout = _QtWidgets.QStackedLayout
QtWidgets.QStackedWidget = _QtWidgets.QStackedWidget
QtWidgets.QStatusBar = _QtWidgets.QStatusBar
QtWidgets.QStyle = _QtWidgets.QStyle
QtWidgets.QStyleFactory = _QtWidgets.QStyleFactory
QtWidgets.QStyleHintReturn = _QtWidgets.QStyleHintReturn
QtWidgets.QStyleHintReturnMask = _QtWidgets.QStyleHintReturnMask
QtWidgets.QStyleHintReturnVariant = _QtWidgets.QStyleHintReturnVariant
QtWidgets.QStyleOption = _QtWidgets.QStyleOption
QtWidgets.QStyleOptionButton = _QtWidgets.QStyleOptionButton
QtWidgets.QStyleOptionComboBox = _QtWidgets.QStyleOptionComboBox
QtWidgets.QStyleOptionComplex = _QtWidgets.QStyleOptionComplex
QtWidgets.QStyleOptionDockWidget = _QtWidgets.QStyleOptionDockWidget
QtWidgets.QStyleOptionFocusRect = _QtWidgets.QStyleOptionFocusRect
QtWidgets.QStyleOptionFrame = _QtWidgets.QStyleOptionFrame
QtWidgets.QStyleOptionGraphicsItem = _QtWidgets.QStyleOptionGraphicsItem
QtWidgets.QStyleOptionGroupBox = _QtWidgets.QStyleOptionGroupBox
QtWidgets.QStyleOptionHeader = _QtWidgets.QStyleOptionHeader
QtWidgets.QStyleOptionMenuItem = _QtWidgets.QStyleOptionMenuItem
QtWidgets.QStyleOptionProgressBar = _QtWidgets.QStyleOptionProgressBar
QtWidgets.QStyleOptionRubberBand = _QtWidgets.QStyleOptionRubberBand
QtWidgets.QStyleOptionSizeGrip = _QtWidgets.QStyleOptionSizeGrip
QtWidgets.QStyleOptionSlider = _QtWidgets.QStyleOptionSlider
QtWidgets.QStyleOptionSpinBox = _QtWidgets.QStyleOptionSpinBox
QtWidgets.QStyleOptionTab = _QtWidgets.QStyleOptionTab
QtWidgets.QStyleOptionTabBarBase = _QtWidgets.QStyleOptionTabBarBase
QtWidgets.QStyleOptionTabWidgetFrame = _QtWidgets.QStyleOptionTabWidgetFrame
QtWidgets.QStyleOptionTitleBar = _QtWidgets.QStyleOptionTitleBar
QtWidgets.QStyleOptionToolBar = _QtWidgets.QStyleOptionToolBar
QtWidgets.QStyleOptionToolBox = _QtWidgets.QStyleOptionToolBox
QtWidgets.QStyleOptionToolButton = _QtWidgets.QStyleOptionToolButton
QtWidgets.QStyleOptionViewItem = _QtWidgets.QStyleOptionViewItem
QtWidgets.QStylePainter = _QtWidgets.QStylePainter
QtWidgets.QStyledItemDelegate = _QtWidgets.QStyledItemDelegate
QtWidgets.QSwipeGesture = _QtWidgets.QSwipeGesture
QtWidgets.QSystemTrayIcon = _QtWidgets.QSystemTrayIcon
QtWidgets.QTabBar = _QtWidgets.QTabBar
QtWidgets.QTabWidget = _QtWidgets.QTabWidget
QtWidgets.QTableView = _QtWidgets.QTableView
QtWidgets.QTableWidget = _QtWidgets.QTableWidget
QtWidgets.QTableWidgetItem = _QtWidgets.QTableWidgetItem
QtWidgets.QTableWidgetSelectionRange = _QtWidgets.QTableWidgetSelectionRange
QtWidgets.QTapAndHoldGesture = _QtWidgets.QTapAndHoldGesture
QtWidgets.QTapGesture = _QtWidgets.QTapGesture
QtWidgets.QTextBrowser = _QtWidgets.QTextBrowser
QtWidgets.QTextEdit = _QtWidgets.QTextEdit
# QtWidgets.QTileRules = _QtWidgets.QTileRules  # Not in PyQt4
QtWidgets.QTimeEdit = _QtWidgets.QTimeEdit
QtWidgets.QToolBar = _QtWidgets.QToolBar
QtWidgets.QToolBox = _QtWidgets.QToolBox
QtWidgets.QToolButton = _QtWidgets.QToolButton
QtWidgets.QToolTip = _QtWidgets.QToolTip
QtWidgets.QTreeView = _QtWidgets.QTreeView
QtWidgets.QTreeWidget = _QtWidgets.QTreeWidget
QtWidgets.QTreeWidgetItem = _QtWidgets.QTreeWidgetItem
QtWidgets.QTreeWidgetItemIterator = _QtWidgets.QTreeWidgetItemIterator
QtWidgets.QUndoCommand = _QtWidgets.QUndoCommand
QtWidgets.QUndoGroup = _QtWidgets.QUndoGroup
QtWidgets.QUndoStack = _QtWidgets.QUndoStack
QtWidgets.QUndoView = _QtWidgets.QUndoView
QtWidgets.QVBoxLayout = _QtWidgets.QVBoxLayout
QtWidgets.QWhatsThis = _QtWidgets.QWhatsThis
QtWidgets.QWidget = _QtWidgets.QWidget
QtWidgets.QWidgetAction = _QtWidgets.QWidgetAction
QtWidgets.QWidgetItem = _QtWidgets.QWidgetItem
QtWidgets.QWizard = _QtWidgets.QWizard
QtWidgets.QWizardPage = _QtWidgets.QWizardPage
QtWidgets.qApp = _QtWidgets.qApp


# QtCore.ClassInfo = _QtCore.ClassInfo  # Not in PyQt4
# QtCore.Connection = _QtCore.Connection  # Not in docs?
# QtCore.MetaFunction = _QtCore.MetaFunction  # Not in PyQt4
QtCore.QAbstractAnimation = _QtCore.QAbstractAnimation
QtCore.QAbstractEventDispatcher = _QtCore.QAbstractEventDispatcher
QtCore.QAbstractItemModel = _QtCore.QAbstractItemModel
QtCore.QAbstractListModel = _QtCore.QAbstractListModel
QtCore.QAbstractState = _QtCore.QAbstractState
QtCore.QAbstractTableModel = _QtCore.QAbstractTableModel
QtCore.QAbstractTransition = _QtCore.QAbstractTransition
QtCore.QAnimationGroup = _QtCore.QAnimationGroup
# QtCore.QBasicMutex = _QtCore.QBasicMutex  # Not in docs?
QtCore.QBasicTimer = _QtCore.QBasicTimer
QtCore.QBitArray = _QtCore.QBitArray
QtCore.QBuffer = _QtCore.QBuffer
QtCore.QByteArray = _QtCore.QByteArray
QtCore.QByteArrayMatcher = _QtCore.QByteArrayMatcher
QtCore.QChildEvent = _QtCore.QChildEvent
QtCore.QCoreApplication = _QtCore.QCoreApplication
QtCore.QCryptographicHash = _QtCore.QCryptographicHash
QtCore.QDataStream = _QtCore.QDataStream
QtCore.QDate = _QtCore.QDate
QtCore.QDateTime = _QtCore.QDateTime
QtCore.QDir = _QtCore.QDir
QtCore.QDirIterator = _QtCore.QDirIterator
QtCore.QDynamicPropertyChangeEvent = _QtCore.QDynamicPropertyChangeEvent
QtCore.QEasingCurve = _QtCore.QEasingCurve
QtCore.QElapsedTimer = _QtCore.QElapsedTimer
QtCore.QEvent = _QtCore.QEvent
QtCore.QEventLoop = _QtCore.QEventLoop
QtCore.QEventTransition = _QtCore.QEventTransition
# QtCore.QFactoryInterface = _QtCore.QFactoryInterface  # Not in PyQt4
QtCore.QFile = _QtCore.QFile
# QtCore.QFileDevice = _QtCore.QFileDevice
QtCore.QFileInfo = _QtCore.QFileInfo
QtCore.QFileSystemWatcher = _QtCore.QFileSystemWatcher
QtCore.QFinalState = _QtCore.QFinalState
QtCore.QGenericArgument = _QtCore.QGenericArgument
QtCore.QGenericReturnArgument = _QtCore.QGenericReturnArgument
QtCore.QHistoryState = _QtCore.QHistoryState
QtCore.QIODevice = _QtCore.QIODevice
# QtCore.QItemSelectionRange = _QtCore.QItemSelectionRange
# QtCore.QJsonArray = _QtCore.QJsonArray
# QtCore.QJsonDocument = _QtCore.QJsonDocument
# QtCore.QJsonParseError = _QtCore.QJsonParseError
# QtCore.QJsonValue = _QtCore.QJsonValue
QtCore.QLibraryInfo = _QtCore.QLibraryInfo
QtCore.QLine = _QtCore.QLine
QtCore.QLineF = _QtCore.QLineF
QtCore.QLocale = _QtCore.QLocale
QtCore.QMargins = _QtCore.QMargins
# QtCore.QMessageLogContext = _QtCore.QMessageLogContext
QtCore.QMetaClassInfo = _QtCore.QMetaClassInfo
QtCore.QMetaEnum = _QtCore.QMetaEnum
QtCore.QMetaMethod = _QtCore.QMetaMethod
QtCore.QMetaObject = _QtCore.QMetaObject
QtCore.QMetaProperty = _QtCore.QMetaProperty
QtCore.QMimeData = _QtCore.QMimeData
QtCore.QModelIndex = _QtCore.QModelIndex
QtCore.QMutex = _QtCore.QMutex
QtCore.QMutexLocker = _QtCore.QMutexLocker
QtCore.QObject = _QtCore.QObject
QtCore.QParallelAnimationGroup = _QtCore.QParallelAnimationGroup
QtCore.QPauseAnimation = _QtCore.QPauseAnimation
QtCore.QPersistentModelIndex = _QtCore.QPersistentModelIndex
QtCore.QPluginLoader = _QtCore.QPluginLoader
QtCore.QPoint = _QtCore.QPoint
QtCore.QPointF = _QtCore.QPointF
QtCore.QProcess = _QtCore.QProcess
QtCore.QProcessEnvironment = _QtCore.QProcessEnvironment
QtCore.QPropertyAnimation = _QtCore.QPropertyAnimation
QtCore.QReadLocker = _QtCore.QReadLocker
QtCore.QReadWriteLock = _QtCore.QReadWriteLock
QtCore.QRect = _QtCore.QRect
QtCore.QRectF = _QtCore.QRectF
QtCore.QRegExp = _QtCore.QRegExp
QtCore.QResource = _QtCore.QResource
QtCore.QRunnable = _QtCore.QRunnable
QtCore.QSemaphore = _QtCore.QSemaphore
QtCore.QSequentialAnimationGroup = _QtCore.QSequentialAnimationGroup
QtCore.QSettings = _QtCore.QSettings
QtCore.QSignalMapper = _QtCore.QSignalMapper
QtCore.QSignalTransition = _QtCore.QSignalTransition
QtCore.QSize = _QtCore.QSize
QtCore.QSizeF = _QtCore.QSizeF
QtCore.QSocketNotifier = _QtCore.QSocketNotifier
QtCore.QState = _QtCore.QState
QtCore.QStateMachine = _QtCore.QStateMachine
QtCore.QSysInfo = _QtCore.QSysInfo
QtCore.QSystemSemaphore = _QtCore.QSystemSemaphore
# QtCore.QT_TRANSLATE_NOOP = _QtCore.QT_TRANSLATE_NOOP  # Not in PyQt4
# QtCore.QT_TRANSLATE_NOOP3 = _QtCore.QT_TRANSLATE_NOOP3  # Not in PyQt4
# QtCore.QT_TRANSLATE_NOOP_UTF8 = _QtCore.QT_TRANSLATE_NOOP_UTF8  # Not in PyQt4
# QtCore.QT_TR_NOOP = _QtCore.QT_TR_NOOP  # Not in PyQt4
# QtCore.QT_TR_NOOP_UTF8 = _QtCore.QT_TR_NOOP_UTF8  # Not in PyQt4
QtCore.QTemporaryFile = _QtCore.QTemporaryFile
QtCore.QTextBoundaryFinder = _QtCore.QTextBoundaryFinder
QtCore.QTextCodec = _QtCore.QTextCodec
QtCore.QTextDecoder = _QtCore.QTextDecoder
QtCore.QTextEncoder = _QtCore.QTextEncoder
QtCore.QTextStream = _QtCore.QTextStream
QtCore.QTextStreamManipulator = _QtCore.QTextStreamManipulator
QtCore.QThread = _QtCore.QThread
QtCore.QThreadPool = _QtCore.QThreadPool
QtCore.QTime = _QtCore.QTime
QtCore.QTimeLine = _QtCore.QTimeLine
QtCore.QTimer = _QtCore.QTimer
QtCore.QTimerEvent = _QtCore.QTimerEvent
QtCore.QTranslator = _QtCore.QTranslator
QtCore.QUrl = _QtCore.QUrl
QtCore.QVariantAnimation = _QtCore.QVariantAnimation
QtCore.QWaitCondition = _QtCore.QWaitCondition
QtCore.QWriteLocker = _QtCore.QWriteLocker
QtCore.QXmlStreamAttribute = _QtCore.QXmlStreamAttribute
QtCore.QXmlStreamAttributes = _QtCore.QXmlStreamAttributes
QtCore.QXmlStreamEntityDeclaration = _QtCore.QXmlStreamEntityDeclaration
QtCore.QXmlStreamEntityResolver = _QtCore.QXmlStreamEntityResolver
QtCore.QXmlStreamNamespaceDeclaration = _QtCore.QXmlStreamNamespaceDeclaration
QtCore.QXmlStreamNotationDeclaration = _QtCore.QXmlStreamNotationDeclaration
QtCore.QXmlStreamReader = _QtCore.QXmlStreamReader
QtCore.QXmlStreamWriter = _QtCore.QXmlStreamWriter
QtCore.Qt = _QtCore.Qt
QtCore.QtCriticalMsg = _QtCore.QtCriticalMsg
QtCore.QtDebugMsg = _QtCore.QtDebugMsg
QtCore.QtFatalMsg = _QtCore.QtFatalMsg
# QtCore.QtInfoMsg = _QtCore.QtInfoMsg  # Not in docs?
QtCore.QtMsgType = _QtCore.QtMsgType
QtCore.QtSystemMsg = _QtCore.QtSystemMsg
QtCore.QtWarningMsg = _QtCore.QtWarningMsg
# QtCore.SIGNAL = _QtCore.SIGNAL  # Not in PyQt5
# QtCore.SLOT = _QtCore.SLOT  # Not in PyQt5
QtCore.qAbs = _QtCore.qAbs
# QtCore.qAcos = _QtCore.qAcos  # Not in PyQt4
QtCore.qAddPostRoutine = _QtCore.qAddPostRoutine
# QtCore.qAsin = _QtCore.qAsin  # Not in PyQt4
# QtCore.qAtan = _QtCore.qAtan  # Not in PyQt4
# QtCore.qAtan2 = _QtCore.qAtan2  # Not in PyQt4
QtCore.qChecksum = _QtCore.qChecksum
QtCore.qCritical = _QtCore.qCritical
QtCore.qDebug = _QtCore.qDebug
# QtCore.qExp = _QtCore.qExp  # Not in PyQt4
# QtCore.qFabs = _QtCore.qFabs   # Not in PyQt4
# QtCore.qFastCos = _QtCore.qFastCos  # Not in PyQt4
# QtCore.qFastSin = _QtCore.qFastSin  # Not in PyQt4
QtCore.qFatal = _QtCore.qFatal
QtCore.qFuzzyCompare = _QtCore.qFuzzyCompare
# QtCore.qFuzzyIsNull = _QtCore.qFuzzyIsNull  # Not in PyQt4
# QtCore.qInstallMessageHandler = _QtCore.qInstallMessageHandler  # Not in docs?
QtCore.qIsFinite = _QtCore.qIsFinite
QtCore.qIsInf = _QtCore.qIsInf
QtCore.qIsNaN = _QtCore.qIsNaN
QtCore.qIsNull = _QtCore.qIsNull
QtCore.qRegisterResourceData = _QtCore.qRegisterResourceData
# QtCore.qTan = _QtCore.qTan  # Not in PyQt4
QtCore.qUnregisterResourceData = _QtCore.qUnregisterResourceData
QtCore.qVersion = _QtCore.qVersion
QtCore.qWarning = _QtCore.qWarning
QtCore.qrand = _QtCore.qrand
QtCore.qsrand = _QtCore.qsrand
# QtCore.qtTrI = _QtCore.qtTrId  # Not in PyQt4


"""

Special case

In some bindings, members are either misplaced or renamed.

"""

if "PySide2" == QtCompat.__binding__:
    QtCore.QAbstractProxyModel = _QtCore.QAbstractProxyModel
    QtCore.QSortFilterProxyModel = _QtCore.QSortFilterProxyModel
    QtCore.QStringListModel = _QtGui.QStringListModel
    QtCore.QItemSelection = _QtCore.QItemSelection
    QtCore.QItemSelectionModel = _QtCore.QItemSelectionModel

if "PyQt5" == QtCompat.__binding__:
    QtCore.QAbstractProxyModel = _QtCore.QAbstractProxyModel
    QtCore.QSortFilterProxyModel = _QtCore.QSortFilterProxyModel
    QtCore.QStringListModel = _QtCore.QStringListModel
    QtCore.QItemSelection = _QtCore.QItemSelection
    QtCore.QItemSelectionModel = _QtCore.QItemSelectionModel

if "PySide" == QtCompat.__binding__:
    QtCore.QAbstractProxyModel = _QtGui.QAbstractProxyModel
    QtCore.QSortFilterProxyModel = _QtGui.QSortFilterProxyModel
    QtCore.QStringListModel = _QtGui.QStringListModel
    QtCore.QItemSelection = _QtGui.QItemSelection
    QtCore.QItemSelectionModel = _QtGui.QItemSelectionModel

if "PyQt4" == QtCompat.__binding__:
    QtCore.QAbstractProxyModel = _QtGui.QAbstractProxyModel
    QtCore.QSortFilterProxyModel = _QtGui.QSortFilterProxyModel
    QtCore.QItemSelection = _QtGui.QItemSelection
    QtCore.QStringListModel = _QtGui.QStringListModel
    QtCore.QItemSelectionModel = _QtGui.QItemSelectionModel

if "PyQt" in QtCompat.__binding__:
    QtCore.Property = _QtCore.pyqtProperty
    QtCore.Signal = _QtCore.pyqtSignal
    QtCore.Slot = _QtCore.pyqtSlot

else:
    QtCore.Property = _QtCore.Property
    QtCore.Signal = _QtCore.Signal
    QtCore.Slot = _QtCore.Slot


# Hide internal members from external use.
del(_QtCore)
del(_QtGui)
del(_QtWidgets)
del(_bindings)
del(_binding)
del(_found_finding)
