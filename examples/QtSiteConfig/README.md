## `QtSiteConfig` example

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

#### QtSiteConfig.py: Adding non-standard modules

This example shows how to add a module that is not included by default with Qt.py.

```python
def update_members_example(members):
    """An example of adding Qsci to Qt.py.
    
    Remove "_example" from the function name to use this example.

    Arguments:
        members (dict): The default list of members in Qt.py.
            Update this dict with any modifications needed.

    """

    if step == 'common':
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


#### QtSiteConfig.py: Standardizing PyQt4 functionality

This example reproduces functionality already in Qt.py but it provides a good example of what is necessary to create your QtCompat namespaces with custom function decorators to change how the source function runs.

```python
def update_members_example(members, step):
    """This function is called by Qt.py to modify the modules it exposes.

    Remove "_example" from the function name to use this example.

    Arguments:
        members (dict): The members considered by Qt.py
        step (str): Used to identify what members will be used for.
    """
    if step == 'compatibility':
        members['PyQt4']["QFileDialog"] = {
            "getOpenFileName": "_QtWidgets.QFileDialog.getOpenFileName",
            "getOpenFileNames": "_QtWidgets.QFileDialog.getOpenFileNames",
            "getSaveFileName": "_QtWidgets.QFileDialog.getSaveFileName",
        }

def update_compatibility_decorators_example(binding, decorators):
    """ This function is called by Qt.py to modify the decorators applied to
    QtCompat namespace objects. Defining this method is optional.

    Remove "_example" from the function name to use this example.

    Arguments:
        binding (str): The Qt binding being wrapped by Qt.py
        decorators (dict): Maps specific decorator functions to
            QtCompat namespace functions. See Qt._build_compatibility_members
            for more info.
    """
    if binding == 'PyQt4':
        # QFileDialog QtCompat decorator
        def _standardizeQFileDialog(some_function):
            """ decorator that makes PyQt4 return conform to other bindings
            """
            def wrapper(*args, **kwargs):
                ret = some_function(*args, **kwargs)
                # PyQt4 only returns the selected filename
                # force the return to conform to all other bindings
                return (ret, '')
            # preserve docstring and name of original function
            wrapper.__doc__ = some_function.__doc__
            wrapper.__name__ = some_function.__name__
            return wrapper
        decorators["getOpenFileName:_QtWidgets.QFileDialog.getOpenFileName"] = \
            _standardizeQFileDialog
        decorators["getOpenFileNames:_QtWidgets.QFileDialog.getOpenFileNames"] = \
            _standardizeQFileDialog
        decorators["getSaveFileName:_QtWidgets.QFileDialog.getSaveFileName"] = \
            _standardizeQFileDialog
```
