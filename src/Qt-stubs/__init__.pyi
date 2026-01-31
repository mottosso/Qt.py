# a subset of the wrapped modules are available directly from this module, without importing
from . import QtCompat as QtCompat
from . import QtCore as QtCore
from . import QtGui as QtGui
from . import QtHelp as QtHelp
from . import QtMultimedia as QtMultimedia
from . import QtMultimediaWidgets as QtMultimediaWidgets
from . import QtNetwork as QtNetwork
from . import QtOpenGL as QtOpenGL
from . import QtPositioning as QtPositioning
from . import QtPrintSupport as QtPrintSupport
from . import QtQml as QtQml
from . import QtQuick as QtQuick
from . import QtQuickWidgets as QtQuickWidgets
from . import QtRemoteObjects as QtRemoteObjects
from . import QtSensors as QtSensors
from . import QtSql as QtSql
from . import QtSvg as QtSvg
from . import QtTest as QtTest
from . import QtWebChannel as QtWebChannel
from . import QtWebSockets as QtWebSockets
from . import QtWidgets as QtWidgets
from . import QtXml as QtXml

__binding__: str
__qt_version__: str
__binding_version__: str
IsPyQt6: bool
IsPyQt5: bool
IsPyQt4: bool
IsPySide: bool
IsPySide2: bool
IsPySide6: bool

QT_VERBOSE: bool
QT_PREFERRED_BINDING: str

class MissingMember: ...

def _warn(text: str) -> None: ...
