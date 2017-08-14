## Docker

In order to successfully test Qt.py against the different bindings of different versions, we use Travis-CI to run Docker containers.

CentOS-based images are built and stored in [Dockerhub](https://hub.docker.com/r/fredrikaverpil/qt.py/tags/). They follow the [VFX Reference Platform specifications](http://www.vfxplatform.com/) with some additionals, and are quite jam-packed.

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

We freeze the code around the time of [SIGGRAPH](http://www.siggraph.org) (usually July/August) each year. This is usually when the VFX Reference Platform is updated.

In order to be able to re-build our images from a certain point in time, we check out commits or download specific source archives rather than going for the always-latest version of software.

There are two rules for choosing the commit SHAs:

- No commit SHA can be newer than the commit SHA from PySide2
- No binding's commit SHA can be older than their respective Qt commit SHA

<br>
<br>


**CY2017 details**

| Software | Details |
| -------- | --------------- |
| PySide2 | [commit](https://codereview.qt-project.org/gitweb?p=pyside/pyside-setup.git;a=commit;h=8913156381b7dc51f903b9e459c143fb25097cab) |
| PySide | [to be decided](https://github.com/pyside/pyside-setup/commits/master) |
| SIP | version 4.18.1 (needs to be supported by both PyQt4 and PyQt5) |
| PyQt5 | version 5.6 |
| PyQt4 | version 4.11.4 |
| Qt5 | [commit](http://code.qt.io/cgit/qt/qt5.git/commit/?h=v5.6.1&id=adf7bcc0b1785c451b06f13c049e5b946b393705) |
| Adsk Qt5 `qtbase` | [commit](https://github.com/autodesk-forks/qtbase/commit/72e3fbb0d27e5d91b1676312ab6a7f6a979ed4e7) |
| Adsk Qt5 `qtx11extras` | [commit](https://github.com/autodesk-forks/qtx11extras/commit/d86b59059f0340f3707dad008a8f632b070de4e6) |
| Qt5 Creator | [commit](http://code.qt.io/cgit/qt-creator/qt-creator.git/commit/?h=v4.0.2&id=47b4f2c73834dd971a5ce418368b5d991d08a666) |
| Qt4 | [to be decided](http://code.qt.io/cgit/qt/qt.git/log/) |

