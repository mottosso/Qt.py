## `QtSiteConfig_platforms` example

This example illustrates how to use QtSiteConfig to give access to platform specific Qt members.

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
