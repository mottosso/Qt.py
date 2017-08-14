## Docker

In order to successfully test Qt.py against the different bindings of different versions, we use Travis-CI to run Docker containers based on [pre-built CentOS-based images](https://hub.docker.com/r/fredrikaverpil/qt.py/tags/).

The Docker images follow the [VFX Reference Platform specifications](http://www.vfxplatform.com/) with some additionals, and are quite jam-packed.


<br>
<br>


**Software built from source**

* glibc
* gcc
* git
* cmake
* Qt4
* Qt5 + Autodesk-modifications
* Qt5 Creator (required for `QtUiTools`)
* SIP
* PyQt4
* PySide
* PyQt5
* PySide2

<br>
<br>


**Software versions**

We use source code from around the time of [SIGGRAPH](http://www.siggraph.org) (usually July/August) each year. This is usually when the VFX Reference Platform is updated.

In order to be able to re-build our images from a certain point in time, we cherry-pick commit SHAs or source archives rather than going for the always-latest version of software. We then set up new images as required and add them to our continous integration tests.

There are two rules for choosing software versions to build:

- No commit SHA can be newer than the commit SHA from PySide2
- No binding's commit SHA can be older than their respective Qt commit SHA

Other noteworthy things:

- PySide cannot be built with anything newer than Python 3.4.
- SIP is used by both PyQt4 and PyQt5 and its version must therefore be chosen carefully.
- PySide2 does not have a maintained `__version__` string.

<br>
<br>


**CY2017 details**

Using YYYY-MM-DD.

| Software | Date | Details |
| -------- | ---- | --------------- |
| PySide2 | 2016-06-03 | [commit](https://codereview.qt-project.org/gitweb?p=pyside/pyside-setup.git;a=commit;h=8913156381b7dc51f903b9e459c143fb25097cab) |
| PySide | latest | [commit log](https://github.com/pyside/pyside-setup/commits/master) |
| SIP | 2016-07-25 | [v4.18.1](https://sourceforge.net/projects/pyqt/files/sip/) |
| PyQt5 | 2016-04-25 | [v5.6](https://sourceforge.net/projects/pyqt/files/PyQt5/) |
| PyQt4 | 2015-08-01 | [v4.11.4](https://sourceforge.net/projects/pyqt/files/PyQt4/) |
| Qt5 | 2016-06-01 | [commit](http://code.qt.io/cgit/qt/qt5.git/commit/?h=v5.6.1&id=adf7bcc0b1785c451b06f13c049e5b946b393705) |
| Adsk Qt5 `qtbase` | 2016-06-28 | [commit](https://github.com/autodesk-forks/qtbase/commit/72e3fbb0d27e5d91b1676312ab6a7f6a979ed4e7) |
| Adsk Qt5 `qtx11extras` | 2016-06-28 | [commit](https://github.com/autodesk-forks/qtx11extras/commit/d86b59059f0340f3707dad008a8f632b070de4e6) |
| Qt5 Creator | 2016-06-09 | [commit](http://code.qt.io/cgit/qt-creator/qt-creator.git/commit/?h=v4.0.2&id=47b4f2c73834dd971a5ce418368b5d991d08a666) |
| Qt4 | latest | [commit log](http://code.qt.io/cgit/qt/qt.git/log/) |
