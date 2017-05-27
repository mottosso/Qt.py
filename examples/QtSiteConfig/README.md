## `QSiteConfig` example

This example illustrates how to make a QtSiteConfig module and how it affects Qt.py at run-time.

<br>

**Usage**

```bash
$ cd to/this/directory
$ python main.py
# Qt.QtCore was successfully removed by QSideConfig.py
```

Because `QtSiteConfig.py` is in the current working directory, it is available to import by Python. If running from a different directory, then you can append this directory to your `PYTHONPATH`

```bash
$ set PYTHONPATH=path/to/QtSiteConfig/
$ python main.py
# Qt.QtCore was successfully removed by QSideConfig.py
```

> Linux and MacOS users: Replace `set` with `export`

<br>

**Advanced example**

If you need to  you can also add modules that are not in the standard Qt.py.

```python
def update_members_example(members):
    """An example of adding QJsonDocument to QtCore and the Qsci.
    
    Remove "_example" from the function name to use this example.

    Arguments:
        members (dict): The default list of members in Qt.py.
            Update this dict and return it with any modifications needed.

    """

    # Include QJsonDocument module
    members["QtCore"].append("QJsonDocument")

    # Include Qsci module for scintilla lexer support.
    members["Qsci"] = [
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
```
