"""Example of Qt_site_config module used to modify exposed members of Qt.py.

INSTALLATION: If you want to use this module it must be named Qt_site_config
and importable by python before Qt.py is first imported. Qt.py attempts to
import Qt_site_config then calls update_common_members. This allows you to
customize available modules for Qt.py without modifying the Qt.py package.
"""


def update_common_members(_common_members):
    """ This function is called by Qt.py to modify the modules it exposes.

    Arguments:
        _common_members (dict): The default list of _common_members in Qt.py.
            Update this dict and return it with any modifications needed.

    Return:
        dict that will be used by Qt.py as _common_members.
    """
    # Contrived example used for unit testing. This makes the QtOpenGL module
    # not accessible. I chose this so it can be tested everywhere, for a more
    # realistic example see update_common_members_example
    del(_common_members["QtOpenGL"])
    return _common_members


def update_common_members_example(_common_members):
    """ A example of adding QJsonDocument to QtCore and the Qsci.
    Remove _example from the function name to use this example.

    Arguments:
        _common_members (dict): The default list of _common_members in Qt.py.
            Update this dict and return it with any modifications needed.

    Return:
        dict that will be used by Qt.py as _common_members.
    """
    # Include QJsonDocument module
    _common_members["QtCore"].append("QJsonDocument")
    # Include Qsci module for scintilla lexer support.
    _common_members["Qsci"] = [
        "QsciAPIs",
        "QsciAbstractAPIs",
        "QsciCommand",
        "QsciCommandSet",
        "QsciDocument",
        "QsciLexer",
        "QsciLexerAVS",
        "QsciLexerBash",
        "QsciLexerBatch",
        "QsciLexerCMake",
        "QsciLexerCPP",
        "QsciLexerCSS",
        "QsciLexerCSharp",
        "QsciLexerCoffeeScript",
        "QsciLexerCustom",
        "QsciLexerD",
        "QsciLexerDiff",
        "QsciLexerFortran",
        "QsciLexerFortran77",
        "QsciLexerHTML",
        "QsciLexerIDL",
        "QsciLexerJSON",
        "QsciLexerJava",
        "QsciLexerJavaScript",
        "QsciLexerLua",
        "QsciLexerMakefile",
        "QsciLexerMarkdown",
        "QsciLexerMatlab",
        "QsciLexerOctave",
        "QsciLexerPO",
        "QsciLexerPOV",
        "QsciLexerPascal",
        "QsciLexerPerl",
        "QsciLexerPostScript",
        "QsciLexerProperties",
        "QsciLexerPython",
        "QsciLexerRuby",
        "QsciLexerSQL",
        "QsciLexerSpice",
        "QsciLexerTCL",
        "QsciLexerTeX",
        "QsciLexerVHDL",
        "QsciLexerVerilog",
        "QsciLexerXML",
        "QsciLexerYAML",
        "QsciMacro",
        "QsciPrinter",
        "QsciScintilla",
        "QsciScintillaBase",
        "QsciStyle",
        "QsciStyledText",
    ]
    return _common_members


def test_add_site_members():
    try:
        from Qt import QtOpenGL
        msg = "Qt.QtOpenGL was importable, update_common_members was not " \
            "applied correctly."
        assert False, msg
        # suppress 'Qt.QtOpenGL' imported but unused warning
        QtOpenGL
    except ImportError:
        "Qt.QtOpenGL was successfully removed by update_common_members."
