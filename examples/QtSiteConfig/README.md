## `QtSiteConfig` example

This example illustrates how to make a QtSiteConfig module and how it affects Qt.py at run-time.

**Usage**

```bash
$ cd to/this/directory
$ python main.py
# Qt.QtCore was successfully removed by QSiteConfig.py
```

Because `QtSiteConfig.py` is in the current working directory, it is available to import by Python. If running from a different directory, then you can append this directory to your `PYTHONPATH`

```bash
$ set PYTHONPATH=path/to/QtSiteConfig/
$ python main.py
# Qt.QtCore was successfully removed by QSiteConfig.py
```

> Linux and MacOS users: Replace `set` with `export`

<br>

**Advanced examples**

If you need to you can also add modules that are not in the standard Qt.py. All of these functions are optional in QtSiteConfig, so only implement the functions you need.

#### QtSiteConfig.py: Adding non-standard modules

By default Qt.py only exposes the "lowest common denominator" of all bindings. This example shows how to add the Qsci module that is not included by default with Qt.py.

```python
def update_members(members):
    """An example of adding Qsci to Qt.py.

    Arguments:
        members (dict): The default list of members in Qt.py.
            Update this dict with any modifications needed.
    """

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


#### QtSiteConfig.py: Standardizing the location of Qt classes

Some classes have been moved to new locations between bindings. Qt.py uses the namespace dictated by PySide2 and most members are already in place.
This example reproduces functionality already in Qt.py but it provides a good example of how use this function.

```python
def update_misplaced_members(members):
    """This optional function is called by Qt.py to standardize the location
    and naming of exposed classes.

    Arguments:
        members (dict): The members considered by Qt.py
    """
    # Standardize the the Property name
    members["PySide2"]["QtCore.Property"] = "QtCore.Property"
    members["PyQt5"]["QtCore.pyqtProperty"] = "QtCore.Property"
    members["PySide"]["QtCore.Property"] = "QtCore.Property"
    members["PyQt4"]["QtCore.pyqtProperty"] = "QtCore.Property"
```

#### QtSiteConfig.py: Standardizing PyQt4's QFileDialog functionality

This example reproduces functionality already in Qt.py but it provides a good example of what is necessary to create your QtCompat namespaces with custom method decorators to change how the source method runs.

```python
def update_compatibility_members(members):
    """This function is called by Qt.py to modify the modules it exposes.

    Arguments:
        members (dict): The members considered by Qt.py
    """
    members['PyQt4']["QFileDialog"] = {
        "getOpenFileName": "QtWidgets.QFileDialog.getOpenFileName",
        "getOpenFileNames": "QtWidgets.QFileDialog.getOpenFileNames",
        "getSaveFileName": "QtWidgets.QFileDialog.getSaveFileName",
    }

def update_compatibility_decorators(binding, decorators):
    """ This function is called by Qt.py to modify the decorators applied to
    QtCompat namespace objects. Defining this method is optional.

    Arguments:
        binding (str): The Qt binding being wrapped by Qt.py
        decorators (dict): Maps specific decorator methods to
            QtCompat namespace methods. See Qt._build_compatibility_members
            for more info.
    """
    if binding == 'PyQt4':
        # QFileDialog QtCompat decorator
        def _standardizeQFileDialog(some_function):
            """ decorator that makes PyQt4 return conform to other bindings
            """
            def wrapper(*args, **kwargs):
                ret = some_function(*args, **kwargs)
                # PyQt4 only returns the selected filename, force it to a
                # standard return of the selected filename, and a empty string
                # for the selected filter
                return (ret, '')
            # preserve docstring and name of original method
            wrapper.__doc__ = some_function.__doc__
            wrapper.__name__ = some_function.__name__
            return wrapper

        decorators.setdefault("QFileDialog",{})["getOpenFileName"] = \
            _standardizeQFileDialog
        decorators.setdefault("QFileDialog",{})["getOpenFileNames"] = \
            _standardizeQFileDialog
        decorators.setdefault("QFileDialog",{})["getSaveFileName"] = \
            _standardizeQFileDialog
```
