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

    Map all bindings to PySide2

    Project goals:
        Qt.py was born in the film and visual effects industry to address
        the growing need for the development of software capable of running
        with more than one flavour of the Qt bindings for Python - PySide,
        PySide2, PyQt4 and PyQt5.

        1. Build for one, run with all
        2. Explicit is better than implicit
        3. Support co-existence

    Default resolution order:
        - PySide2
        - PyQt5
        - PySide
        - PyQt4

    Usage:
        >> import sys
        >> from Qt import QtWidgets
        >> app = QtWidgets.QApplication(sys.argv)
        >> button = QtWidgets.QPushButton("Hello World")
        >> button.show()
        >> app.exec_()

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

__all__ = ["QtGui", "QtCore", "QtWidgets", "QtCompat"]

# Flags from environment variables

# Enable additional output when loading Qt.py
QT_VERBOSE = bool(os.getenv("QT_VERBOSE"))
QT_PREFERRED_BINDING = os.getenv("QT_PREFERRED_BINDING")
QT_STRICT = bool(os.getenv("QT_STRICT"))

# Supported submodules
QtGui = types.ModuleType("QtGui")
QtCore = types.ModuleType("QtCore")
QtWidgets = types.ModuleType("QtWidgets")
QtCompat = types.ModuleType("QtCompat")


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
    except AttributeError as e:
        raise ImportError(str(e))
        # PyQt4 < v4.6
    except ValueError as e:
        # API version already set to v1
        raise ImportError(str(e))

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

_log("Preferred bindings: %s" % list(_b.__name__ for _b in _bindings))


_found_binding = False
for _binding in _bindings:
    _log("Trying %s" % _binding.__name__)

    try:
        _QtCore, _QtGui, _QtWidgets = _binding()
        _found_binding = True
        break

    except ImportError as e:
        _log("ImportError: %s" % e)
        continue

if not _found_binding:
    # If not binding were found, throw this error
    raise ImportError("No Qt binding were found.")


def _convert(lines):
    """Convert compiled .ui file from PySide2 to Qt.py

    Arguments:
        lines (list): Each line of of .ui file

    Usage:
        >> with open("myui.py") as f:
        ..   lines = _convert(f.readlines())

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
            lines = _convert(f.readlines())

        backup = "%s_backup%s" % os.path.splitext(args.convert)
        sys.stdout.write("Creating \"%s\"..\n" % backup)
        shutil.copy(args.convert, backup)

        #
        # <------ Write
        #
        with open(args.convert, "w") as f:
            f.write("".join(lines))

        sys.stdout.write("Successfully converted \"%s\"\n" % args.convert)


_members = {
    "QtGui": [
        "QAbstractTextDocumentLayout",
        "QActionEvent",
        "QBitmap",
        "QBrush",
        "QClipboard",
        "QCloseEvent",
        "QColor",
        "QConicalGradient",
        "QContextMenuEvent",
        "QCursor",
        "QDoubleValidator",
        "QDrag",
        "QDragEnterEvent",
        "QDragLeaveEvent",
        "QDragMoveEvent",
        "QDropEvent",
        "QFileOpenEvent",
        "QFocusEvent",
        "QFont",
        "QFontDatabase",
        "QFontInfo",
        "QFontMetrics",
        "QFontMetricsF",
        "QGradient",
        "QHelpEvent",
        "QHideEvent",
        "QHoverEvent",
        "QIcon",
        "QIconDragEvent",
        "QIconEngine",
        "QImage",
        "QImageIOHandler",
        "QImageReader",
        "QImageWriter",
        "QInputEvent",
        "QInputMethodEvent",
        "QIntValidator",
        "QKeyEvent",
        "QKeySequence",
        "QLinearGradient",
        "QMatrix2x2",
        "QMatrix2x3",
        "QMatrix2x4",
        "QMatrix3x2",
        "QMatrix3x3",
        "QMatrix3x4",
        "QMatrix4x2",
        "QMatrix4x3",
        "QMatrix4x4",
        "QMouseEvent",
        "QMoveEvent",
        "QMovie",
        "QPaintDevice",
        "QPaintEngine",
        "QPaintEngineState",
        "QPaintEvent",
        "QPainter",
        "QPainterPath",
        "QPainterPathStroker",
        "QPalette",
        "QPen",
        "QPicture",
        "QPictureIO",
        "QPixmap",
        "QPixmapCache",
        "QPolygon",
        "QPolygonF",
        "QQuaternion",
        "QRadialGradient",
        "QRegExpValidator",
        "QRegion",
        "QResizeEvent",
        "QSessionManager",
        "QShortcutEvent",
        "QShowEvent",
        "QStandardItem",
        "QStandardItemModel",
        "QStatusTipEvent",
        "QSyntaxHighlighter",
        "QTabletEvent",
        "QTextBlock",
        "QTextBlockFormat",
        "QTextBlockGroup",
        "QTextBlockUserData",
        "QTextCharFormat",
        "QTextCursor",
        "QTextDocument",
        "QTextDocumentFragment",
        "QTextFormat",
        "QTextFragment",
        "QTextFrame",
        "QTextFrameFormat",
        "QTextImageFormat",
        "QTextInlineObject",
        "QTextItem",
        "QTextLayout",
        "QTextLength",
        "QTextLine",
        "QTextList",
        "QTextListFormat",
        "QTextObject",
        "QTextObjectInterface",
        "QTextOption",
        "QTextTable",
        "QTextTableCell",
        "QTextTableCellFormat",
        "QTextTableFormat",
        "QTransform",
        "QValidator",
        "QVector2D",
        "QVector3D",
        "QVector4D",
        "QWhatsThisClickedEvent",
        "QWheelEvent",
        "QWindowStateChangeEvent",
        "qAlpha",
        "qBlue",
        "qGray",
        "qGreen",
        "qIsGray",
        "qRed",
        "qRgb",
        "qRgb",
    ],
    "QtWidgets": [
        "QAbstractButton",
        "QAbstractGraphicsShapeItem",
        "QAbstractItemDelegate",
        "QAbstractItemView",
        "QAbstractScrollArea",
        "QAbstractSlider",
        "QAbstractSpinBox",
        "QAction",
        "QActionGroup",
        "QApplication",
        "QBoxLayout",
        "QButtonGroup",
        "QCalendarWidget",
        "QCheckBox",
        "QColorDialog",
        "QColumnView",
        "QComboBox",
        "QCommandLinkButton",
        "QCommonStyle",
        "QCompleter",
        "QDataWidgetMapper",
        "QDateEdit",
        "QDateTimeEdit",
        "QDesktopWidget",
        "QDial",
        "QDialog",
        "QDialogButtonBox",
        "QDirModel",
        "QDockWidget",
        "QDoubleSpinBox",
        "QErrorMessage",
        "QFileDialog",
        "QFileIconProvider",
        "QFileSystemModel",
        "QFocusFrame",
        "QFontComboBox",
        "QFontDialog",
        "QFormLayout",
        "QFrame",
        "QGesture",
        "QGestureEvent",
        "QGestureRecognizer",
        "QGraphicsAnchor",
        "QGraphicsAnchorLayout",
        "QGraphicsBlurEffect",
        "QGraphicsColorizeEffect",
        "QGraphicsDropShadowEffect",
        "QGraphicsEffect",
        "QGraphicsEllipseItem",
        "QGraphicsGridLayout",
        "QGraphicsItem",
        # "QGraphicsItemAnimation",  # Not in PyQt4
        "QGraphicsItemGroup",
        "QGraphicsLayout",
        "QGraphicsLayoutItem",
        "QGraphicsLineItem",
        "QGraphicsLinearLayout",
        "QGraphicsObject",
        "QGraphicsOpacityEffect",
        "QGraphicsPathItem",
        "QGraphicsPixmapItem",
        "QGraphicsPolygonItem",
        "QGraphicsProxyWidget",
        "QGraphicsRectItem",
        "QGraphicsRotation",
        "QGraphicsScale",
        "QGraphicsScene",
        "QGraphicsSceneContextMenuEvent",
        "QGraphicsSceneDragDropEvent",
        "QGraphicsSceneEvent",
        "QGraphicsSceneHelpEvent",
        "QGraphicsSceneHoverEvent",
        "QGraphicsSceneMouseEvent",
        "QGraphicsSceneMoveEvent",
        "QGraphicsSceneResizeEvent",
        "QGraphicsSceneWheelEvent",
        "QGraphicsSimpleTextItem",
        "QGraphicsTextItem",
        "QGraphicsTransform",
        "QGraphicsView",
        "QGraphicsWidget",
        "QGridLayout",
        "QGroupBox",
        "QHBoxLayout",
        "QHeaderView",
        "QInputDialog",
        "QItemDelegate",
        "QItemEditorCreatorBase",
        "QItemEditorFactory",
        "QKeyEventTransition",
        "QLCDNumber",
        "QLabel",
        "QLayout",
        "QLayoutItem",
        "QLineEdit",
        "QListView",
        "QListWidget",
        "QListWidgetItem",
        "QMainWindow",
        "QMdiArea",
        "QMdiSubWindow",
        "QMenu",
        "QMenuBar",
        "QMessageBox",
        "QMouseEventTransition",
        "QPanGesture",
        "QPinchGesture",
        "QPlainTextDocumentLayout",
        "QPlainTextEdit",
        "QProgressBar",
        "QProgressDialog",
        "QPushButton",
        "QRadioButton",
        "QRubberBand",
        "QScrollArea",
        "QScrollBar",
        "QShortcut",
        "QSizeGrip",
        "QSizePolicy",
        "QSlider",
        "QSpacerItem",
        "QSpinBox",
        "QSplashScreen",
        "QSplitter",
        "QSplitterHandle",
        "QStackedLayout",
        "QStackedWidget",
        "QStatusBar",
        "QStyle",
        "QStyleFactory",
        "QStyleHintReturn",
        "QStyleHintReturnMask",
        "QStyleHintReturnVariant",
        "QStyleOption",
        "QStyleOptionButton",
        "QStyleOptionComboBox",
        "QStyleOptionComplex",
        "QStyleOptionDockWidget",
        "QStyleOptionFocusRect",
        "QStyleOptionFrame",
        "QStyleOptionGraphicsItem",
        "QStyleOptionGroupBox",
        "QStyleOptionHeader",
        "QStyleOptionMenuItem",
        "QStyleOptionProgressBar",
        "QStyleOptionRubberBand",
        "QStyleOptionSizeGrip",
        "QStyleOptionSlider",
        "QStyleOptionSpinBox",
        "QStyleOptionTab",
        "QStyleOptionTabBarBase",
        "QStyleOptionTabWidgetFrame",
        "QStyleOptionTitleBar",
        "QStyleOptionToolBar",
        "QStyleOptionToolBox",
        "QStyleOptionToolButton",
        "QStyleOptionViewItem",
        "QStylePainter",
        "QStyledItemDelegate",
        "QSwipeGesture",
        "QSystemTrayIcon",
        "QTabBar",
        "QTabWidget",
        "QTableView",
        "QTableWidget",
        "QTableWidgetItem",
        "QTableWidgetSelectionRange",
        "QTapAndHoldGesture",
        "QTapGesture",
        "QTextBrowser",
        "QTextEdit",
        "QTimeEdit",
        "QToolBar",
        "QToolBox",
        "QToolButton",
        "QToolTip",
        "QTreeView",
        "QTreeWidget",
        "QTreeWidgetItem",
        "QTreeWidgetItemIterator",
        "QUndoCommand",
        "QUndoGroup",
        "QUndoStack",
        "QUndoView",
        "QVBoxLayout",
        "QWhatsThis",
        "QWidget",
        "QWidgetAction",
        "QWidgetItem",
        "QWizard",
        "QWizardPage",
    ],

    "QtCore": [
        "QAbstractAnimation",
        "QAbstractEventDispatcher",
        "QAbstractItemModel",
        "QAbstractListModel",
        "QAbstractState",
        "QAbstractTableModel",
        "QAbstractTransition",
        "QAnimationGroup",
        "QBasicTimer",
        "QBitArray",
        "QBuffer",
        "QByteArray",
        "QByteArrayMatcher",
        "QChildEvent",
        "QCoreApplication",
        "QCryptographicHash",
        "QDataStream",
        "QDate",
        "QDateTime",
        "QDir",
        "QDirIterator",
        "QDynamicPropertyChangeEvent",
        "QEasingCurve",
        "QElapsedTimer",
        "QEvent",
        "QEventLoop",
        "QEventTransition",
        "QFile",
        "QFileInfo",
        "QFileSystemWatcher",
        "QFinalState",
        "QGenericArgument",
        "QGenericReturnArgument",
        "QHistoryState",
        "QIODevice",
        "QLibraryInfo",
        "QLine",
        "QLineF",
        "QLocale",
        "QMargins",
        "QMetaClassInfo",
        "QMetaEnum",
        "QMetaMethod",
        "QMetaObject",
        "QMetaProperty",
        "QMimeData",
        "QModelIndex",
        "QMutex",
        "QMutexLocker",
        "QObject",
        "QParallelAnimationGroup",
        "QPauseAnimation",
        "QPersistentModelIndex",
        "QPluginLoader",
        "QPoint",
        "QPointF",
        "QProcess",
        "QProcessEnvironment",
        "QPropertyAnimation",
        "QReadLocker",
        "QReadWriteLock",
        "QRect",
        "QRectF",
        "QRegExp",
        "QResource",
        "QRunnable",
        "QSemaphore",
        "QSequentialAnimationGroup",
        "QSettings",
        "QSignalMapper",
        "QSignalTransition",
        "QSize",
        "QSizeF",
        "QSocketNotifier",
        "QState",
        "QStateMachine",
        "QSysInfo",
        "QSystemSemaphore",
        "QTemporaryFile",
        "QTextBoundaryFinder",
        "QTextCodec",
        "QTextDecoder",
        "QTextEncoder",
        "QTextStream",
        "QTextStreamManipulator",
        "QThread",
        "QThreadPool",
        "QTime",
        "QTimeLine",
        "QTimer",
        "QTimerEvent",
        "QTranslator",
        "QUrl",
        "QVariantAnimation",
        "QWaitCondition",
        "QWriteLocker",
        "QXmlStreamAttribute",
        "QXmlStreamAttributes",
        "QXmlStreamEntityDeclaration",
        "QXmlStreamEntityResolver",
        "QXmlStreamNamespaceDeclaration",
        "QXmlStreamNotationDeclaration",
        "QXmlStreamReader",
        "QXmlStreamWriter",
        "Qt",
        "QtCriticalMsg",
        "QtDebugMsg",
        "QtFatalMsg",
        "QtMsgType",
        "QtSystemMsg",
        "QtWarningMsg",
        "qAbs",
        "qAddPostRoutine",
        "qChecksum",
        "qCritical",
        "qDebug",
        "qFatal",
        "qFuzzyCompare",
        "qIsFinite",
        "qIsInf",
        "qIsNaN",
        "qIsNull",
        "qRegisterResourceData",
        "qUnregisterResourceData",
        "qVersion",
        "qWarning",
        "qrand",
        "qsrand",
    ]
}

QtCompat.__version__ = "0.7.0"
QtCompat._cli = _cli
QtCompat._convert = _convert

QtCompat.__added__ = list()     # DEPRECATED
QtCompat.__remapped__ = list()  # DEPRECATED
QtCompat.__modified__ = list()  # DEPRECATED
QtCompat.__wrapper_version__ = "0.7.0"  # DEPRECATED

if QT_STRICT:
    for _module, _members in _members.items():
        for _member in _members:
            _original = getattr(sys.modules[__name__], "_%s" % _module)
            _replacement = getattr(sys.modules[__name__], _module)
            setattr(_replacement, _member, getattr(_original, _member))

else:
    # Plain reference to original modules
    QtWidgets = _QtWidgets
    QtGui = _QtGui
    QtCore = _QtCore

# Enable direct import of submodules
# E.g. import Qt.QtCore
sys.modules.update({
    __name__ + ".QtGui": QtGui,
    __name__ + ".QtCore": QtCore,
    __name__ + ".QtWidgets": QtWidgets,
    __name__ + ".QtCompat": QtCompat,
})


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
del(_found_binding)
