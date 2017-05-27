## `siteMembers` examples

When Qt.py is first imported it attempts to import the QtSiteConfig module. This module is optional and does not need to exist. If it exists it must implement the `update_common_members` function.

```python
def update_common_members(_common_members):
    """ This is the minimum requirements for this module """
    return _common_members
```
And if you wanted to remove the QtOpenGL module you could implement.
```python
def update_common_members(_common_members):
    del(_common_members["QtOpenGL"])
    return _common_members
```

If you need to  you can also add modules that are not in the standard Qt.py.
```python
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
```
