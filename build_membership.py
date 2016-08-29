

def build_membership():
    """Generate a .json file with all members of PySide2"""

    # NOTE: PySide2, as of this writing, is incomplete.
    # In it's __all__ module is a module, `QtOpenGL`
    # that does no exists. This causes `import *` to fail.

    import json
    from PySide2 import __all__
    __all__.remove("QtOpenGL")

    # These modules do not exist pre-Qt 5,
    # so do not bother testing for them.
    __all__.remove("QtSql")
    __all__.remove("QtSvg")

    from PySide2 import *

    # Serialise members
    members = {}
    for name, module in locals().copy().items():
        if name.startswith("_"):
            continue

        if name in ("json", "members"):
            continue

        members[name] = dir(module)

    # Write to disk
    with open("reference_members.json", "w") as f:
        json.dump(members, f, indent=4)


def build_tests():
    """Build membership tests

    Members only available in Qt 5 are excluded, along with member
    exclusive to a paricular binding.

    """

    header = """\
import os
import sys
import json

with open("reference_members.json") as f:
    reference_members = json.load(f)

excluded = {

    "QtCore": [
        #
        # From PySide
        #
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

        #
        # From PyQt4
        #
        "ClassInfo",
        "MetaFunction",
        "QFactoryInterface",
        "QSortFilterProxyModel",
        "QStringListModel",
        "QT_TRANSLATE_NOOP3",
        "QT_TRANSLATE_NOOP_UTF8",
        "__moduleShutdown",
        "__version__",
        "__version_info__",
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

        #
        # From PyQt5
        #
        "SIGNAL",
        "SLOT",
    ],

    "QtGui": [
        #
        # From PySide
        #
        "QGuiApplication",
        "QPagedPaintDevice",
        "QSurface",
        "QSurfaceFormat",
        "QTouchDevice",
        "QWindow",

        #
        #  From PyQt4
        #
        "QAccessibleEvent",
        "QToolBarChangeEvent",

        #
        #  From PyQt5
        #
        "QMatrix",
        "QPyTextObject",
        "QStringListModel",
    ],

    "QtWebKit": [
        #
        # From PyQt4
        #
        "WebCore",

        #
        # From PyQt5
        #
        "__doc__",
        "__file__",
        "__name__",
        "__package__",
    ],

    "QtScript": [
        #
        # From PyQt4
        #
        "QScriptExtensionInterface",
        "QScriptExtensionPlugin",
        "QScriptProgram",
        "QScriptable",

        #
        # From PyQt5
        #
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
        #
        # PyQt4
        #
        "QIPv6Address",
    ],
}

"""

    test = """\
def test_{binding}_members():
    os.environ["QT_PREFERRED_BINDING"] = "{Binding}"

    from Qt import *

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

    tests = list(test.format(Binding=binding, binding=binding.lower())
                 for binding in ["PyQt5",
                                 "PyQt4",
                                 "PySide"])

    with open("test_membership.py", "w") as f:
        contents = header + "\n".join(tests)
        print(contents)  # Preview content during tests
        f.write(contents)


if __name__ == '__main__':
    build_membership()
    build_tests()
