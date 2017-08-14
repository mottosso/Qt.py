import json


def build_membership():
    """Generate a .json file with all members of PySide2"""

    # NOTE: PySide2, as of this writing, is incomplete.
    # In it's __all__ module is a module, `QtOpenGL`
    # that does no exists. This causes `import *` to fail.

    from PySide2 import __all__
    __all__.remove("QtOpenGL")

    # These modules do not exist pre-Qt 5,
    # so do not bother testing for them.
    __all__.remove("QtSql")
    __all__.remove("QtSvg")

    # These should be present in PySide2,
    # but are not as of this writing.
    for missing in ("QtWidgets",
                    "QtXml",
                    "QtHelp",
                    "QtPrintSupport"):
        __all__.append(missing)

    # Why `import *`?
    #
    # PySide, and PyQt, perform magic that triggers via Python's
    # import mechanism. If we try and sidestep it in any way, say
    # by using `imp.load_module` or `__import__`, the mechanism
    # will not trigger and the compiled libraries will not get loaded.
    #
    # Wildcard was the only way I could think of to import everything,
    # without hardcoding the members, such as QtCore into the function.
    from PySide2 import *

    # Serialise members
    members = {}
    for name, module in locals().copy().items():
        if name.startswith("_"):
            continue

        if name in ("json", "members", "missing"):
            continue

        members[name] = list(member for member in dir(module)
                             if not member.startswith("_"))

    # Write to disk
    with open("reference_members.json", "w") as f:
        json.dump(members, f, indent=4)


def build_tests():
    """Build membership tests

    Members only available in Qt 5 are excluded, along with member
    exclusive to a paricular binding.

    """

    header = """\
#
# AUTOMATICALLY GENERATED MEMBERSHIP TEST, DO NOT MODIFY
#

import os
import json


with open("reference_members.json") as f:
    reference_members = json.load(f)

# Only bother checking strict mode, as it is
# the only mode that modifies membership in any way.
os.environ["QT_STRICT"] = "1"

excluded = {excluded}

""".format(excluded=json.dumps(excluded, indent=4))

    test = """\
def test_{binding}_members():
    os.environ["QT_PREFERRED_BINDING"] = "{Binding}"

    # Initialise Qt.py, this is especially important for PyQt4
    # which sets sip to 2.0 upon loading Qt.py
    import Qt

    if "PyQt" in "{Binding}":
        # PyQt4 and 5 performs some magic here
        # that must take place before attempting
        # to import with wildcard.
        from {Binding} import Qt as _

    if "PySide2" == "{Binding}":
        # PySide2, as of this writing, doesn't include
        # these modules in it's __all__ list; leaving
        # the wildcard import below untrue.
        from Qt import __all__
        for missing in ("QtWidgets",
                        "QtXml",
                        "QtHelp",
                        "QtNetwork",
                        "QtPrintSupport"):
            __all__.append(missing)

    from Qt import *

    if "PySide" == "{Binding}":
        # TODO: This needs a more robust implementation.
        from Qt import QtWidgets

    target_members = dict()
    for name, module in locals().copy().items():
        if name.startswith("_"):
            continue

        target_members[name] = dir(module)

    missing = dict()
    for module, members in reference_members.items():
        for member in members:

            # Ignore those that have no Qt 4-equivalent.
            if member in excluded.get(module, []):
                continue

            if member not in target_members.get(module, []):
                if module not in missing:
                    missing[module] = []
                missing[module].append(member)

    message = ""
    for module, members in missing.items():
        message += "\\n%s: \\n - %s" % (module, "\\n - ".join(members))

    assert not missing, "{Binding} is missing members: %s" % message

"""

    tests = list(test.format(Binding=binding,
                             binding=binding.lower())
                 for binding in ["PyQt5",
                                 "PyQt4",
                                 "PySide"])

    with open("test_membership.py", "w") as f:
        contents = header + "\n".join(tests)
        f.write(contents)


# Do not consider these members.
#
# Some of these are either:
# 1. Unique to a particular binding
# 2. Unique to Qt 5
# 3. Not yet included in PySide2
#
# TODO: Clearly mark which are which. (3) should
#   eventually be removed from this dictionary.
excluded = {
    "QtCore": [
        # missing from PySide
        "Connection",
        "QBasicMutex",
        "QFileDevice",
        "QItemSelectionRange",
        "QJsonArray",
        "QJsonDocument",
        "QJsonParseError",
        "QJsonValue",
        "QMessageLogContext",
        "QtInfoMsg",
        "qInstallMessageHandler",
        "QT_TRANSLATE_NOOP",
        "QT_TR_NOOP",
        "QT_TR_NOOP_UTF8",

        # missing from PyQt4
        "ClassInfo",
        "MetaFunction",
        "QFactoryInterface",
        "QSortFilterProxyModel",
        "QStringListModel",
        "QT_TRANSLATE_NOOP3",
        "QT_TRANSLATE_NOOP_UTF8",
        "__moduleShutdown",
        "__version__",  # (2) unique to PyQt
        "__version_info__",  # (2) unique to PyQt
        "qAcos",
        "qAsin",
        "qAtan",
        "qAtan2",
        "qExp",
        "qFabs",
        "qFastCos",
        "qFastSin",
        "qFuzzyIsNull",
        "qTan",
        "qtTrId",

        # missing from all bindings
        "QFileSelector",
        "QMimeDatabase",
        "QMimeType",

        # missing from PyQt5
        "SIGNAL",
        "SLOT",
    ],

    "QtGui": [
        # missing from PySide
        "QGuiApplication",  # (2) unique to Qt 5
        "QPagedPaintDevice",
        "QSurface",
        "QSurfaceFormat",
        "QTouchDevice",
        "QWindow",  # (2) unique to Qt 5
        "QTouchEvent",  # (2) unique to Qt 5
        "qRgba",  # (2) unique to Qt 5

        # missing from PyQt4
        "QAccessibleEvent",
        "QToolBarChangeEvent",

        # missing from PyQt5
        "QMatrix",
        "QPyTextObject",
        "QStringListModel",

        # missing from all bindings
        "QAccessible",
        "QAccessibleInterface",
        "QExposeEvent",
        "QOpenGLContext",
        "QOpenGLFramebufferObject",
        "QOpenGLShader",
        "QOpenGLBuffer",
        "QScreen",
    ],

    "QtWebKit": [
        # missing from PyQt4
        "WebCore",

        # missing from PyQt5
        "__doc__",
        "__file__",
        "__name__",
        "__package__",
    ],

    "QtScript": [
        # missing from PyQt4
        "QScriptExtensionInterface",
        "QScriptExtensionPlugin",
        "QScriptProgram",
        "QScriptable",

        # missing from PyQt5
        "QScriptClass",
        "QScriptClassPropertyIterator",
        "QScriptContext",
        "QScriptContextInfo",
        "QScriptEngine",
        "QScriptEngineAgent",
        "QScriptString",
        "QScriptValue",
        "QScriptValueIterator",
        "__doc__",
        "__file__",
        "__name__",
        "__package__",
    ],

    "QtNetwork": [
        # missing from Qt 4
        "QIPv6Address",
    ],

    "QtPrintSupport": [
        # PyQt4
        "QAbstractPrintDialog",
        "QPageSetupDialog",
        "QPrintDialog",
        "QPrintEngine",
        "QPrintPreviewDialog",
        "QPrintPreviewWidget",
        "QPrinter",
        "QPrinterInfo",
    ],

    "QtWidgets": [
        # PyQt4
        "QTileRules",

        # PyQt5
        "QGraphicsItemAnimation",
        "QTileRules",

        "qApp",  # See Issue #171
    ],

    "QtHelp": [
        # PySide
        "QHelpContentItem",
        "QHelpContentModel",
        "QHelpContentWidget",
        "QHelpEngine",
        "QHelpEngineCore",
        "QHelpIndexModel",
        "QHelpIndexWidget",
        "QHelpSearchEngine",
        "QHelpSearchQuery",
        "QHelpSearchQueryWidget",
        "QHelpSearchResultWidget",
    ],

    "QtXml": [
        # PySide
        "QDomAttr",
        "QDomCDATASection",
        "QDomCharacterData",
        "QDomComment",
        "QDomDocument",
        "QDomDocumentFragment",
        "QDomDocumentType",
        "QDomElement",
        "QDomEntity",
        "QDomEntityReference",
        "QDomImplementation",
        "QDomNamedNodeMap",
        "QDomNode",
        "QDomNodeList",
        "QDomNotation",
        "QDomProcessingInstruction",
        "QDomText",
        "QXmlAttributes",
        "QXmlContentHandler",
        "QXmlDTDHandler",
        "QXmlDeclHandler",
        "QXmlDefaultHandler",
        "QXmlEntityResolver",
        "QXmlErrorHandler",
        "QXmlInputSource",
        "QXmlLexicalHandler",
        "QXmlLocator",
        "QXmlNamespaceSupport",
        "QXmlParseException",
        "QXmlReader",
        "QXmlSimpleReader",
    ],

    "QtTest": [
        # missing from PySide
        "QTest",
    ],
}

if __name__ == '__main__':
    build_membership()
    build_tests()
