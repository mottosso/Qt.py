## Docker

In order to successfully test Qt.py against the different bindings of different versions, we use Travis-CI to run Docker containers based on [pre-built CentOS-based images](https://hub.docker.com/r/fredrikaverpil/qt.py/tags/).

The Docker images follow the [VFX Reference Platform specifications](http://www.vfxplatform.com/) with some additionals, and are quite jam-packed.


<br>
<br>


**Software built from source**

* glibc<sup>1</sup>
* gcc<sup>1</sup>
* git<sup>2</sup>
* cmake<sup>3</sup>
* Qt4<sup>4</sup>
* Qt5 + Autodesk-modifications<sup>1</sup>
* Qt5 Creator<sup>1, 5</sup>
* SIP<sup>4</sup>
* PyQt4<sup>4</sup>
* PySide<sup>4, 6</sup>
* PyQt5<sup>1</sup>
* PySide2<sup>1</sup>

<sup>1</sup> Per specification from VFX Platform  
<sup>2</sup> Adds possibility to faster clone large repositories  
<sup>3</sup> cmake 3.x required to build PySide2  
<sup>4</sup> Required for Qt.py testing  
<sup>5</sup> Required for `PySide2.QtUiTools`
<sup>6</sup> A [fork of PySide](https://github.com/fredrikaverpil/pyside-setup) is used, where Python version check is removed

<br>
<br>


**Software versions**

We use source code from around the time of [SIGGRAPH](http://www.siggraph.org) (usually July/August) each year. This is usually when the VFX Reference Platform is updated.

In order to be able to re-build our images from a certain point in time, we cherry-pick commit SHAs or source archives rather than going for the always-latest version of software. We then set up new images as required and add them to our continous integration tests.

There are non-strict rules (guidelines) for choosing software versions to build:

- No commit SHA can be newer than the commit SHA from PySide2
- No binding's commit SHA can be older than their respective Qt commit SHA

Other noteworthy things:

- PySide cannot be built with anything newer than Python 3.4, but this version check was removed in the PySide fork used.
- SIP is used by both PyQt4 and PyQt5 and its version must therefore be chosen carefully.
- PySide2 does not have a maintained `__version__` string.

<br>
<br>

**Image tagging**

A new image should be tagged like `repo/qt.py:YYYY`. For CY2017, this translates into `fredrikaverpil/qt.py:2017`.

If there happens to be an update inbetween VFX Platform specifications, a revision version number could be added: `repo/qt.py:YYYY-update1`.

<br>
<br>


**CY2017 details**

| Software | Date | Details |
| -------- | ---- | --------------- |
| PySide2 | 2016-06-03 | [commit](https://codereview.qt-project.org/gitweb?p=pyside/pyside-setup.git;a=commit;h=8913156381b7dc51f903b9e459c143fb25097cab) |
| PySide | latest (fork) | [commit log](https://github.com/fredrikaverpil/pyside-setup/commits/master) |
| SIP | 2016-07-25 | [v4.18.1](https://sourceforge.net/projects/pyqt/files/sip/) |
| PyQt5 | 2016-04-25 | [v5.6](https://sourceforge.net/projects/pyqt/files/PyQt5/) |
| PyQt4 | 2015-08-01 | [v4.11.4](https://sourceforge.net/projects/pyqt/files/PyQt4/) |
| Python 2.7 | 2015-12-05 | [v2.7.11](https://www.python.org/downloads/source/) |
| Python 3.4 | 2016-06-27 | [v3.4.5](https://www.python.org/downloads/source/) |
| Python 3.5 | 2015-12-07 | [v3.5.1](https://www.python.org/downloads/source/) |
| Qt5 | 2016-06-01 | [commit](http://code.qt.io/cgit/qt/qt5.git/commit/?h=v5.6.1&id=adf7bcc0b1785c451b06f13c049e5b946b393705) |
| Adsk Qt5 `qtbase` | 2016-06-28 | [commit](https://github.com/autodesk-forks/qtbase/commit/72e3fbb0d27e5d91b1676312ab6a7f6a979ed4e7) |
| Adsk Qt5 `qtx11extras` | 2016-06-28 | [commit](https://github.com/autodesk-forks/qtx11extras/commit/d86b59059f0340f3707dad008a8f632b070de4e6) |
| Qt5 Creator | 2016-06-09 | [commit](http://code.qt.io/cgit/qt-creator/qt-creator.git/commit/?h=v4.0.2&id=47b4f2c73834dd971a5ce418368b5d991d08a666) |
| Qt4 | latest | [commit log](http://code.qt.io/cgit/qt/qt.git/log/) |
| cmake | 2016-04-15 | [v3.5.2](https://cmake.org/files/) |
| glibc | 2010 (pre-installed in CentOS 6) | 2.12.x |
| gcc | 2014-05-12 | [v4.8.3](ftp://ftp.gnu.org/pub/gnu/gcc/) |

