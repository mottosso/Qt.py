

FROM centos:6

RUN yum install deltarpm -y && \
    yum update -y && \
    # glibc requirements
        yum groupinstall -y "Development tools" && \
    yum install -y \
        # cmake3 requirements
            epel-release && \
    # yum install -y \
    #     # PySide2 requirement
    #         cmake3 && \
    yum install -y \
        # glibc requirements
        glibc-devel.i686 glibc-i686 sudo \

        # Qt5 requirements
            # http://doc.qt.io/qt-5/linux-requirements.html
                libXrender* libxcb* xcb* fontconfig* freetype* libXi* libXext* libX11* libSM* libICE* libglib* libpthread* gstreamer* \
            # https://wiki.qt.io/Building_Qt_5_from_Git
                # Build essentials
                    perl-version \
                # Libxcb
                    libxcb libxcb-devel xcb-util xcb-util-devel xcb-util-*-devel libX11-devel libXrender-devel libXi-devel \
                # Accessibility
                    at-spi2-core-devel \
                    libdbus* \
                # QtWebkit
                    flex bison gperf libicu-devel libxslt-devel ruby \
                # QtMultimedia
                    alsa-lib alsa-lib-devel gstreamer gstreamer-devel gstreamer-plugins-base gstreamer-plugins-base-devel \
                # libICU
                    libicu-devel \
        # QtQuick requirements; OpenGL
        # https://access.redhat.com/solutions/56301
            mesa-libGL mesa-libGL-devel \
        # QtWebEngine requirements (disabled because of error during make)
            # http://doc.qt.io/qt-5/qtwebengine-platform-notes.html
                # bison* flex* gperf* \
                # python2-pkgconfig \
                    # dbus dbus-devel \
                    # fontconfig-devel \
                # libxcb* \
                    # libdrm* \
                    # libXcomposite-devel \
                    # libXcursor-devel \
                    # libXi libXi-devel \
                    # libXrandr-devel \
                    # libXScrnSaver-devel \
                    # libXtst-devel \
                # Note: khr package ???
                # libcap* \
            # https://wiki.qt.io/How_to_Try_QtWebEngine
                # gyp ninja-build \
                # mesa-libEGL-devel libgcrypt-devel libgcrypt pciutils-devel nss-devel libXtst-devel gperf \
                # cups-devel pulseaudio-libs-devel libgudev1-devel systemd-devel libcap-devel alsa-lib-devel flex bison ruby \
                # ninja requirements (used by QtWebEngine)
                    # re2c \
            # https://wiki.qt.io/Building_Qt_5_from_Git
                # libgcrypt-devel libgcrypt pciutils-devel nss-devel libXtst-devel gperf cups-devel pulseaudio-libs-devel libgudev1-devel systemd-devel libcap-devel alsa-lib-devel flex bison ruby gcc-c++ dbus libXrandr-devel libXcomposite-devel libXcursor-devel dbus-devel fontconfig-devel \
        # Python requirements
            zlib-devel openssl-devel sqlite-devel bzip2-devel readline-devel tk-devel \
            valgrind-devel \
        # PySide2 requirements
            # https://wiki.qt.io/PySide2_GettingStarted
                libxslt libxml2 libxml2-devel libxslt-devel cmake3 openssl* \
        # PySide
            # cmake gcc gcc-c++ make python-devel python-pip \
            libxml2-devel libxslt-devel rpmdevtools \
        # Xvfb etc
            Xvfb \
            xorg-x11-server-Xvfb \
            mesa-dri-drivers \
            libxkbcommon \
            libxkbcommon-devel \
            libxkbcommon-x11 \
            libxkbcommon-x11-devel \
        # Git
            # gcc \
            curl-devel expat-devel gettext-devel openssl-devel zlib-devel \
            perl-ExtUtils-MakeMaker \
        # dbus
        dbus \
        # general
        xz wget \
        && \
    yum clean all

# Parallel build processes (set to cores +1)
ENV BUILD_THREADS=17

WORKDIR /workdir


# # glibc (disabled since CentOS 6 comes with glibc 2.12 already)
# # https://github.com/FezVrasta/ark-server-tools/wiki/Install-of-required-versions-of-glibc-and-gcc-on-RHEL-CentOS
# ENV GLIBC_VER=2.12.2
# RUN wget http://ftp.gnu.org/gnu/glibc/glibc-${GLIBC_VER}.tar.gz && \
#     tar -xvzf glibc-${GLIBC_VER}.tar.gz && \
#     cd glibc-${GLIBC_VER} && \
#     mkdir glibc-build && \
#     cd glibc-build && \
#     ../configure --prefix='/usr' && \
#     make -j ${BUILD_THREADS} && \
#     sudo make install && \
#     cd .. && rm -rf glibc-${GLIBC_VER} && rm -f *.tar.gz


# Gcc
# https://github.com/FezVrasta/ark-server-tools/wiki/Install-of-required-versions-of-glibc-and-gcc-on-RHEL-CentOS
# https://gcc.gnu.org/install/configure.html
ENV GCC_VER=4.8.3
RUN \
    wget ftp://ftp.gnu.org/pub/gnu/gcc/gcc-${GCC_VER}/gcc-${GCC_VER}.tar.bz2 && \
    tar xvfj gcc-${GCC_VER}.tar.bz2 && \
    cd gcc-${GCC_VER} && \
    ./contrib/download_prerequisites && \
    mkdir objdir && \
    cd objdir && \
    ../configure --prefix=/usr/local/gcc-${GCC_VER} --enable-languages=c,c++ && \
    make -j ${BUILD_THREADS} && \
    make install && \
    mv /usr/lib64/libstdc++.so.6 /usr/lib64/libstdc++.so.6.bak && \
    mv /usr/local/gcc-${GCC_VER}/lib64/libstdc++.so.6 /usr/lib64/libstdc++.so.6 && \
    mv /usr/local/gcc-${GCC_VER}/lib64/libstdc++.so.6.0.19 /usr/lib64/libstdc++.so.6.0.19 && \
    rm -rf /workdir/*
ENV PATH="/usr/local/gcc-${GCC_VER}/bin:${PATH}"
ENV CC=/usr/local/gcc-${GCC_VER}/bin/gcc
ENV CXX=/usr/local/gcc-${GCC_VER}/bin/g++


# # Check gcc version
# RUN gcc --version
# # Check glibc
# RUN ldd --version


# Cmake3
# https://cmake.org/install/
# https://cmake.org/files/
ENV CMAKE_VER=3.5.2
RUN \
    wget https://cmake.org/files/v3.5/cmake-${CMAKE_VER}.tar.gz && \
    tar xzf cmake-${CMAKE_VER}.tar.gz && \
    cd cmake-${CMAKE_VER} && \
    ./bootstrap && \
    make && \
    make install && \
    rm -rf /workdir/*


# # Check cmake version
# RUN cmake --version


# Git 2.14 with "git clone --jobs" functionality and "git checkout --recurse-submodules"
# https://tecadmin.net/install-git-2-0-on-centos-rhel-fedora/
# https://stackoverflow.com/a/44249558/2448495
ENV GIT_VER=2.14.1
RUN \
    wget https://www.kernel.org/pub/software/scm/git/git-${GIT_VER}.tar.gz && \
    tar xzf git-${GIT_VER}.tar.gz && \
    cd git-${GIT_VER} && \
    make -j${BUILD_THREADS} prefix=/usr/local/git all && \
    make prefix=/usr/local/git install && \
    rm -rf /workdir/*
ENV PATH="/usr/local/git/bin:${PATH}"


# Qt 4.8
# http://doc.qt.io/qt-4.8/requirements-x11.html
# Commits: http://code.qt.io/cgit/qt/qt.git/log/
ENV QT4_VER=4.8
ENV QT4_GIT_COMMIT=0a2f2382541424726168804be2c90b91381608c6
RUN \
    git clone --recursive --jobs ${BUILD_THREADS} --branch ${QT4_VER} https://code.qt.io/qt/qt.git && \
    cd qt && \
    git checkout ${QT4_GIT_COMMIT} && \
    git submodule update --init --recursive && \
   ./configure \
        -opensource \
        -confirm-license \
        -nomake examples \
        -nomake tests && \
    make -j${BUILD_THREADS} && \
    # Install
    make install && \
    # Clean up
    rm -rf /workdir/*


# Qt 5.6.1, Autodesk-modified (cannot be newer than PySide2 commit SHA)
# Qt5 5.6 git commits: http://code.qt.io/cgit/qt/qt5.git/log/?h=5.6
# Autodesk qtbase git commits: https://github.com/autodesk-forks/qtbase/commits/adsk-contrib/vfx/5.6.1
# Autodesk qtx11extras git commits: https://github.com/autodesk-forks/qtx11extras/commits/adsk-contrib/vfx/5.6.1
# ---
# Commits:
# Qt5: http://code.qt.io/cgit/qt/qt5.git/commit/?h=v5.6.1&id=adf7bcc0b1785c451b06f13c049e5b946b393705
# Adsk qtbase: https://github.com/autodesk-forks/qtbase/commit/72e3fbb0d27e5d91b1676312ab6a7f6a979ed4e7
# Adsk qtx11extras: https://github.com/autodesk-forks/qtx11extras/commit/d86b59059f0340f3707dad008a8f632b070de4e6
ENV QT5_VER=5.6.1
ENV QT5_GIT_COMMIT=adf7bcc0b1785c451b06f13c049e5b946b393705
ENV ADSK_QTBASE_GIT_COMMIT=72e3fbb0d27e5d91b1676312ab6a7f6a979ed4e7
ENV ADSK_QTX11EXTRAS_GIT_COMMIT=d86b59059f0340f3707dad008a8f632b070de4e6
RUN \
    git clone --recursive --jobs ${BUILD_THREADS} --branch ${QT5_VER} https://code.qt.io/qt/qt5.git && \
    # Revert to commit SHA
    cd /workdir/qt5 && \
    git checkout ${QT5_GIT_COMMIT} && \
    git submodule update --init --recursive && \
    # Remove qtbase, qtx11extras
    cd /workdir && \
    rm -rf /workdir/qt5/qtbase && \
    rm -rf /workdir/qt5/qtx11extras && \
    # Clone Autodesk's qtbase, qtx11extras
    cd /workdir && \
    mkdir -p /workdir/adsk && \
    git clone --recursive --branch adsk-contrib/vfx/${QT5_VER} https://github.com/autodesk-forks/qtbase.git /workdir/adsk/qtbase && \
    git clone --recursive --branch adsk-contrib/vfx/${QT5_VER} https://github.com/autodesk-forks/qtx11extras.git /workdir/adsk/qtx11extras && \
    # Revert to commit SHA for qtbase
    cd /workdir/adsk/qtbase && \
    git checkout ${ADSK_QTBASE_GIT_COMMIT} && \
    # Revert to commit SHA for qtx11extras
    cd /workdir/adsk/qtx11extras && \
    git checkout ${ADSK_QTX11EXTRAS_GIT_COMMIT} && \
    # Move Autodesk sources into qt5
    mv /workdir/adsk/qtbase /workdir/qt5 && \
    mv /workdir/adsk/qtx11extras /workdir/qt5 && \
    # Build
    cd /workdir/qt5 && \
    # ./configure -help && \
    ./configure \
        -opensource \
        -confirm-license \
        -nomake examples \
        -nomake tests && \
    make -j${BUILD_THREADS} && \
    # Install
    make install && \
    # Clean up
    rm -rf /workdir/*


# Qt5 Creator (cannot be newer than PySide2 commit SHA)
# https://wiki.qt.io/Building_Qt_Creator_from_Git
# Required for PySide2.QtUiTools
# qt-creator git commits: http://code.qt.io/cgit/qt-creator/qt-creator.git/log/?h=4.0
# Commit: http://code.qt.io/cgit/qt-creator/qt-creator.git/commit/?h=v4.0.2&id=47b4f2c73834dd971a5ce418368b5d991d08a666
ENV QT5CREATOR_VER=4.0
ENV QT5CREATOR_GIT_COMMIT=47b4f2c73834dd971a5ce418368b5d991d08a666
RUN \
    git clone --recursive --branch ${QT5CREATOR_VER} --jobs ${BUILD_THREADS} https://code.qt.io/qt-creator/qt-creator.git && \
    cd /workdir/qt-creator && \
    git checkout ${QT5CREATOR_GIT_COMMIT} && \
    git submodule update --init --recursive && \
    mkdir /workdir/qt-creator-build && \
    cd /workdir/qt-creator-build && \
    /usr/local/Qt-${QT5_VER}/bin/qmake -r /workdir/qt-creator/qtcreator.pro && \
    make -j${BUILD_THREADS} && \
    make install INSTALL_ROOT=/usr/local/qtcreator && \
    rm -rf /workdir/*


# Python
# Notes:
#     https://danieleriksson.net/2017/02/08/how-to-install-latest-python-on-centos/
#     http://blog.dscpl.com.au/2015/06/installing-custom-python-version-into.html
#     https://stackoverflow.com/questions/37345044/issue-with-installing-python-2-7-8-alongside-2-7-5-on-rhel-7-2
#
ENV PYTHON27_VER_FULL=2.7.11
ENV PYTHON27_VER=2.7
ENV PYTHON34_VER_FULL=3.4.5
ENV PYTHON34_VER=3.4
ENV PYTHON35_VER_FULL=3.5.1
ENV PYTHON35_VER=3.5
RUN \
    # Python 2
    mkdir -p /usr/local/python${PYTHON27_VER}/lib && \
    wget https://www.python.org/ftp/python/${PYTHON27_VER_FULL}/Python-${PYTHON27_VER_FULL}.tgz && \
    tar xzf Python-${PYTHON27_VER_FULL}.tgz && \
    cd Python-${PYTHON27_VER_FULL} && \
    # Get the configure arguments from an already existing CentOS 7-installation:
    # $ python
    # >>> from distutils.sysconfig import get_config_var
    # >>> print get_config_var('CONFIG_ARGS')
    ./configure \
        --prefix=/usr/local/python${PYTHON27_VER} \
        --enable-shared \
        --enable-unicode=ucs4 \
        LDFLAGS="-Wl,-rpath /usr/local/python${PYTHON27_VER}/lib" \

        --build=x86_64-redhat-linux-gnu \
        --host=x86_64-redhat-linux-gnu \
        --enable-ipv6 \
        --with-dbmliborder=gdbm:ndbm:bdb \
        --with-system-expat \
        --with-system-ffi \
        --with-valgrind \
        build_alias=x86_64-redhat-linux-gnu \
        host_alias=x86_64-redhat-linux-gnu \
        CC=gcc \
        CFLAGS="-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic -D_GNU_SOURCE -fPIC -fwrapv" \
        CPPFLAGS="-I/usr/lib64/libffi-3.0.5/include" && \
    make -j${BUILD_THREADS} && \
    make altinstall && \
    cd /workdir && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    /usr/local/python${PYTHON27_VER}/bin/python${PYTHON27_VER} get-pip.py && \
    /usr/local/python${PYTHON27_VER}/bin/pip${PYTHON27_VER} install -U pip && \
    rm -rf /workdir/* && \

    # Python 3.4
    cd /workdir && \
    mkdir -p /usr/local/python${PYTHON34_VER}/lib && \
    wget https://www.python.org/ftp/python/${PYTHON34_VER_FULL}/Python-${PYTHON34_VER_FULL}.tgz && \
    tar xzf Python-${PYTHON34_VER_FULL}.tgz && \
    cd Python-${PYTHON34_VER_FULL} && \
    # Get the configure arguments from an already existing CentOS 7-installation:
    # $ python
    # >>> from distutils.sysconfig import get_config_var
    # >>> print(get_config_var('CONFIG_ARGS'))
    ./configure \
        --prefix=/usr/local/python${PYTHON34_VER} \
        --enable-shared \
        LDFLAGS="-Wl,-rpath /usr/local/python${PYTHON34_VER}/lib" \

        --build=x86_64-redhat-linux-gnu \
        --host=x86_64-redhat-linux-gnu \
        --enable-ipv6 \
        --with-computed-gotos=yes \
        --with-dbmliborder=gdbm:ndbm:bdb \
        --with-system-expat \
        --with-system-ffi \
        --with-valgrind \
        --without-ensurepip \
        build_alias=x86_64-redhat-linux-gnu \
        host_alias=x86_64-redhat-linux-gnu \
        CC=gcc \
        CFLAGS="-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic -D_GNU_SOURCE -fPIC -fwrapv" \
        CPPFLAGS="-I/usr/lib64/libffi-3.0.5/include" \
        PKG_CONFIG_PATH=":/usr/lib64/pkgconfig:/usr/share/pkgconfig" && \
    make -j${BUILD_THREADS} && \
    make altinstall && \
    cd /workdir && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    /usr/local/python${PYTHON34_VER}/bin/python${PYTHON34_VER} get-pip.py && \
    /usr/local/python${PYTHON34_VER}/bin/pip${PYTHON34_VER} install -U pip && \
    rm -rf /workdir/* && \

    # Python 3.5
    cd /workdir && \
    mkdir -p /usr/local/python${PYTHON35_VER}/lib && \
    wget https://www.python.org/ftp/python/${PYTHON35_VER_FULL}/Python-${PYTHON35_VER_FULL}.tgz && \
    tar xzf Python-${PYTHON35_VER_FULL}.tgz && \
    cd Python-${PYTHON35_VER_FULL} && \
    # Get the configure arguments from an already existing CentOS 7-installation:
    # $ python
    # >>> from distutils.sysconfig import get_config_var
    # >>> print(get_config_var('CONFIG_ARGS'))
    ./configure \
        --prefix=/usr/local/python${PYTHON35_VER} \
        --enable-shared \
        LDFLAGS="-Wl,-rpath /usr/local/python${PYTHON35_VER}/lib" \

        --build=x86_64-redhat-linux-gnu \
        --host=x86_64-redhat-linux-gnu \
        --enable-ipv6 \
        --with-computed-gotos=yes \
        --with-dbmliborder=gdbm:ndbm:bdb \
        --with-system-expat \
        --with-system-ffi \
        --with-valgrind \
        --without-ensurepip \
        build_alias=x86_64-redhat-linux-gnu \
        host_alias=x86_64-redhat-linux-gnu \
        CC=gcc \
        CFLAGS="-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic -D_GNU_SOURCE -fPIC -fwrapv" \
        CPPFLAGS="-I/usr/lib64/libffi-3.0.5/include" \
        PKG_CONFIG_PATH=":/usr/lib64/pkgconfig:/usr/share/pkgconfig" && \
    make -j${BUILD_THREADS} && \
    make altinstall && \
    cd /workdir && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    /usr/local/python${PYTHON35_VER}/bin/python${PYTHON35_VER} get-pip.py && \
    /usr/local/python${PYTHON35_VER}/bin/pip${PYTHON35_VER} install -U pip && \
    rm -rf /workdir/*


# Register Python as default (without replacing system-python and without breaking e.g. yum)
RUN \
    # Python 2.7
    ln -s /usr/local/python${PYTHON27_VER}/bin/python${PYTHON27_VER} /usr/local/bin/python && \
    ln -s /usr/local/python${PYTHON27_VER}/bin/python${PYTHON27_VER} /usr/local/bin/python${PYTHON27_VER} && \
    ln -s /usr/local/python${PYTHON27_VER}/bin/pip${PYTHON27_VER} /usr/local/bin/pip && \
    ln -s /usr/local/python${PYTHON27_VER}/bin/pip${PYTHON27_VER} /usr/local/bin/pip${PYTHON27_VER} && \
    # Python 3.4
    ln -s /usr/local/python${PYTHON34_VER}/bin/python${PYTHON34_VER} /usr/local/bin/python${PYTHON34_VER} && \
    ln -s /usr/local/python${PYTHON34_VER}/bin/pip${PYTHON34_VER} /usr/local/bin/pip${PYTHON34_VER} && \
    # Python 3.5
    ln -s /usr/local/python${PYTHON35_VER}/bin/python${PYTHON35_VER} /usr/local/bin/python${PYTHON35_VER} && \
    ln -s /usr/local/python${PYTHON35_VER}/bin/pip${PYTHON35_VER} /usr/local/bin/pip${PYTHON35_VER}
ENV PATH="/usr/local/bin:${PATH}"


# Pip packages
RUN \
    # Python 2.7
    pip${PYTHON27_VER} install -U \
        # Qt.py testing (nosepipe etc)
        nose \
        nosepipe \
        six \
        packaging \
        # General build
        setuptools \
        wheel && \
    ln -s /usr/local/python${PYTHON27_VER}/bin/nosetests /usr/local/bin/nosetests${PYTHON27_VER} && \

    # Python 3.4
    pip${PYTHON34_VER} install -U \
        # Qt.py testing (nosepipe etc)
        nose \
        nosepipe \
        six \
        packaging \
        # General build
        setuptools \
        wheel && \
    ln -s /usr/local/python${PYTHON34_VER}/bin/nosetests /usr/local/bin/nosetests${PYTHON34_VER} && \

    # Python 3.5
    pip${PYTHON35_VER} install -U \
        # Qt.py testing (nosepipe etc)
        nose \
        nosepipe \
        six \
        packaging \
        # General build
        setuptools \
        wheel && \
    ln -s /usr/local/python${PYTHON35_VER}/bin/nosetests /usr/local/bin/nosetests${PYTHON35_VER}


# Sip (for PyQt4 and PyQt5)
# http://pyqt.sourceforge.net/Docs/sip4/
ENV SIP_VER=4.18.1
RUN \
    # Python 2.7
    wget http://sourceforge.net/projects/pyqt/files/sip/sip-${SIP_VER}/sip-${SIP_VER}.tar.gz && \
    tar -xvf sip-${SIP_VER}.tar.gz && \
    cd sip-${SIP_VER} && \
    python${PYTHON27_VER} configure.py && \
    make -j${BUILD_THREADS} && \
    make install && \
    rm -rf /workdir/* && \

    # Python 3.4
    cd /workdir && \
    wget http://sourceforge.net/projects/pyqt/files/sip/sip-${SIP_VER}/sip-${SIP_VER}.tar.gz && \
    tar -xvf sip-${SIP_VER}.tar.gz && \
    cd sip-${SIP_VER} && \
    python${PYTHON34_VER} configure.py && \
    make -j${BUILD_THREADS} && \
    make install && \
    rm -rf /workdir/* && \

    # Python 3.5
    cd /workdir && \
    wget http://sourceforge.net/projects/pyqt/files/sip/sip-${SIP_VER}/sip-${SIP_VER}.tar.gz && \
    tar -xvf sip-${SIP_VER}.tar.gz && \
    cd sip-${SIP_VER} && \
    python${PYTHON35_VER} configure.py && \
    make -j${BUILD_THREADS} && \
    make install && \
    rm -rf /workdir/*


# PyQt4
# The version of PyQt4 must be compatible with the SIP version used to build PyQt5
# http://pyqt.sourceforge.net/Docs/PyQt4/installation.html
ENV PYQT4_VER=4.11.4
RUN \
    # PyQt4 for Python 2
    wget http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-${PYQT4_VER}/PyQt-x11-gpl-${PYQT4_VER}.tar.gz && \
    tar -xvf PyQt-x11-gpl-${PYQT4_VER}.tar.gz && \
    cd PyQt-x11-gpl-${PYQT4_VER} && \
    # python${PYTHON27_VER} configure-ng.py \
    python${PYTHON27_VER} configure.py \
        # --verbose \
        --confirm-license \
        # --qmake=/usr/bin/qmake-qt4 \
        --qmake=/usr/local/Trolltech/Qt-4.8.7/bin/qmake && \
        # --sip=/usr/local/python${PYTHON27_VER}/bin/sip && \
    make -j${BUILD_THREADS} && \
    make install && \
    rm -rf /workdir/* && \

    # PyQt4 for Python 3.4
    cd /workdir && \
    wget http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-${PYQT4_VER}/PyQt-x11-gpl-${PYQT4_VER}.tar.gz && \
    tar -xvf PyQt-x11-gpl-${PYQT4_VER}.tar.gz && \
    cd PyQt-x11-gpl-${PYQT4_VER} && \
    # python${PYTHON34_VER} configure-ng.py \
    python${PYTHON34_VER} configure.py \
        # --verbose \
        --confirm-license \
        # --qmake=/usr/bin/qmake-qt4 \
        --qmake=/usr/local/Trolltech/Qt-4.8.7/bin/qmake && \
        # --sip=/usr/local/python${PYTHON27_VER}/bin/sip && \
    make -j${BUILD_THREADS} && \
    make install && \
    rm -rf /workdir/* && \

    # PyQt4 for Python 3.5
    cd /workdir && \
    wget http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-${PYQT4_VER}/PyQt-x11-gpl-${PYQT4_VER}.tar.gz && \
    tar -xvf PyQt-x11-gpl-${PYQT4_VER}.tar.gz && \
    cd PyQt-x11-gpl-${PYQT4_VER} && \
    # python${PYTHON35_VER} configure-ng.py \
    python${PYTHON35_VER} configure.py \
        # --verbose \
        --confirm-license \
        # --qmake=/usr/bin/qmake-qt4 \
        --qmake=/usr/local/Trolltech/Qt-4.8.7/bin/qmake && \
        # --sip=/usr/local/python${PYTHON27_VER}/bin/sip && \
    make -j${BUILD_THREADS} && \
    make install && \
    rm -rf /workdir/*


# PySide
# Note: requires cmake3
# http://pyside.readthedocs.io/en/latest/building/options.html
# PySide commits: https://github.com/pyside/pyside-setup/commits/master
# Commit: https://github.com/pyside/pyside-setup/commit/7860bda363438e96fa9e810def0858635a9766cc
ENV PYSIDE_GIT_COMMIT=7860bda363438e96fa9e810def0858635a9766cc
RUN \
    # PySide for Python 2
    git clone --recursive --jobs ${BUILD_THREADS} https://github.com/fredrikaverpil/pyside-setup.git && \
    cd pyside-setup && \
    git checkout ${PYSIDE_GIT_COMMIT} && \
    git submodule update --init --recursive && \
    python${PYTHON27_VER} setup.py \
        install \
            --qmake=/usr/local/Trolltech/Qt-4.8.7/bin/qmake \
            --cmake=/usr/local/bin/cmake \
            --openssl=/usr/bin/openssl \
            --jobs=${BUILD_THREADS} && \
    rm -rf /workdir/* && \

    # PySide for Python 3.4
    cd /workdir && \
    git clone --recursive --jobs ${BUILD_THREADS} https://github.com/fredrikaverpil/pyside-setup.git && \
    cd pyside-setup && \
    git checkout ${PYSIDE_GIT_COMMIT} && \
    git submodule update --init --recursive && \
    python${PYTHON34_VER} setup.py \
        install \
            --qmake=/usr/local/Trolltech/Qt-4.8.7/bin/qmake \
            --cmake=/usr/local/bin/cmake \
            --openssl=/usr/bin/openssl \
            --jobs=${BUILD_THREADS} && \
    rm -rf /workdir/*
# Ugly fix to make PySide find the Qt4 libs
ENV LD_LIBRARY_PATH="/usr/local/Trolltech/Qt-4.8.7/lib:${LD_LIBRARY_PATH}"


# PyQt5
# http://pyqt.sourceforge.net/Docs/PyQt5/installation.html#building-and-installing-from-source
ENV PYQT5_VER=5.6
RUN \
    # PyQt5 for Python 2
    wget http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-${PYQT5_VER}/PyQt5_gpl-${PYQT5_VER}.tar.gz && \
    tar -xvf PyQt5_gpl-${PYQT5_VER}.tar.gz && \
    cd PyQt5_gpl-${PYQT5_VER} && \
    python${PYTHON27_VER} configure.py \
        # --verbose \
        --confirm-license \
        --qmake=/usr/local/Qt-${QT5_VER}/bin/qmake \
        --sip=/usr/local/python${PYTHON27_VER}/bin/sip && \
    make -j${BUILD_THREADS} && \
    make install && \
    rm -rf /workdir/* && \

    # PyQt5 for Python 3.4
    cd /workdir && \
    wget http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-${PYQT5_VER}/PyQt5_gpl-${PYQT5_VER}.tar.gz && \
    tar -xvf PyQt5_gpl-${PYQT5_VER}.tar.gz && \
    cd PyQt5_gpl-${PYQT5_VER} && \
    python${PYTHON34_VER} configure.py \
        # --verbose \
        --confirm-license \
        --qmake=/usr/local/Qt-${QT5_VER}/bin/qmake \
        --sip=/usr/local/python${PYTHON34_VER}/bin/sip && \
    make -j${BUILD_THREADS} && \
    make install && \
    rm -rf /workdir/* && \

    # PyQt5 for Python 3.5
    cd /workdir && \
    wget http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-${PYQT5_VER}/PyQt5_gpl-${PYQT5_VER}.tar.gz && \
    tar -xvf PyQt5_gpl-${PYQT5_VER}.tar.gz && \
    cd PyQt5_gpl-${PYQT5_VER} && \
    python${PYTHON35_VER} configure.py \
        # --verbose \
        --confirm-license \
        --qmake=/usr/local/Qt-${QT5_VER}/bin/qmake \
        --sip=/usr/local/python${PYTHON35_VER}/bin/sip && \
    make -j${BUILD_THREADS} && \
    make install && \
    rm -rf /workdir/*


# PySide2 (has no maintained semantic versioning)
# PySide2 5.6 git commits: https://codereview.qt-project.org/gitweb?p=pyside/pyside-setup.git;a=shortlog;h=refs/heads/5.6
# PySide2: https://codereview.qt-project.org/gitweb?p=pyside/pyside-setup.git;a=commit;h=8913156381b7dc51f903b9e459c143fb25097cab
ENV PYSIDE2_GIT_BRANCH=5.6
ENV PYSIDE2_GIT_COMMIT=8913156381b7dc51f903b9e459c143fb25097cab
RUN \
    # PySide2 for Python 2
    git clone --recursive --jobs ${BUILD_THREADS} --branch ${PYSIDE2_GIT_BRANCH} https://codereview.qt-project.org/pyside/pyside-setup && \
    cd pyside-setup && \
    git checkout ${PYSIDE2_GIT_COMMIT} && \
    git submodule update --init --recursive && \

    # Fix bug in order to build PySide2.QtUiTools: https://bugreports.qt.io/browse/PYSIDE-552
    # sed -i.bak $'s/if(Qt5Designer_FOUND)/find_package(Qt5Designer)\\\nif(Qt5Designer_FOUND)/g' sources/pyside2/CMakeLists.txt && \
    # cat sources/pyside2/CMakeLists.txt && \

    # Fix bug https://bugreports.qt.io/browse/PYSIDE-357
    sed -i -e "s~\b\(packages\b.*\)],~\1, 'pyside2uic.Compiler', 'pyside2uic.port_v' + str(sys.version_info[0])],~" setup.py && \
    # cat setup.py && \

    python${PYTHON27_VER} setup.py \
        # bdist_wheel \
        install \
            --ignore-git \
            --qmake=/usr/local/Qt-${QT5_VER}/bin/qmake \
            --cmake=/usr/local/bin/cmake \
            --openssl=/usr/bin/openssl \
            --jobs=${BUILD_THREADS} && \
    # pip install /workdir/pyside-setup/dist/*.whl
    rm -rf /workdir/* && \

    # PySide2 for Python 3.4
    cd /workdir && \
    git clone --recursive --jobs ${BUILD_THREADS} --branch ${PYSIDE2_GIT_BRANCH} https://codereview.qt-project.org/pyside/pyside-setup && \
    cd pyside-setup && \
    git checkout ${PYSIDE2_GIT_COMMIT} && \
    git submodule update --init --recursive && \

    # Fix bug in order to build PySide2.QtUiTools: https://bugreports.qt.io/browse/PYSIDE-552
    # sed -i.bak $'s/if(Qt5Designer_FOUND)/find_package(Qt5Designer)\\\nif(Qt5Designer_FOUND)/g' sources/pyside2/CMakeLists.txt && \
    # cat sources/pyside2/CMakeLists.txt && \

    # Fix bug https://bugreports.qt.io/browse/PYSIDE-357
    sed -i -e "s~\b\(packages\b.*\)],~\1, 'pyside2uic.Compiler', 'pyside2uic.port_v' + str(sys.version_info[0])],~" setup.py && \
    # cat setup.py && \

    python${PYTHON34_VER} setup.py \
        # bdist_wheel \
        install \
            --ignore-git \
            --qmake=/usr/local/Qt-${QT5_VER}/bin/qmake \
            --cmake=/usr/local/bin/cmake \
            --openssl=/usr/bin/openssl \
            --jobs=${BUILD_THREADS} && \
    # pip install /workdir/pyside-setup/dist/*.whl
    rm -rf /workdir/* && \

    # PySide2 for Python 3.5
    cd /workdir && \
    git clone --recursive --jobs ${BUILD_THREADS} --branch ${PYSIDE2_GIT_BRANCH} https://codereview.qt-project.org/pyside/pyside-setup && \
    cd pyside-setup && \
    git checkout ${PYSIDE2_GIT_COMMIT} && \
    git submodule update --init --recursive && \

    # Fix bug in order to build PySide2.QtUiTools: https://bugreports.qt.io/browse/PYSIDE-552
    # sed -i.bak $'s/if(Qt5Designer_FOUND)/find_package(Qt5Designer)\\\nif(Qt5Designer_FOUND)/g' sources/pyside2/CMakeLists.txt && \
    # cat sources/pyside2/CMakeLists.txt && \

    # Fix bug https://bugreports.qt.io/browse/PYSIDE-357
    sed -i -e "s~\b\(packages\b.*\)],~\1, 'pyside2uic.Compiler', 'pyside2uic.port_v' + str(sys.version_info[0])],~" setup.py && \
    # cat setup.py && \

    python${PYTHON35_VER} setup.py \
        # bdist_wheel \
        install \
            --ignore-git \
            --qmake=/usr/local/Qt-${QT5_VER}/bin/qmake \
            --cmake=/usr/local/bin/cmake \
            --openssl=/usr/bin/openssl \
            --jobs=${BUILD_THREADS} && \
    # pip install /workdir/pyside-setup/dist/*.whl
    rm -rf /workdir/*
# Ugly fix to make PySide2 find the Qt5 libs
ENV LD_LIBRARY_PATH="/usr/local/Qt-${QT5_VER}/lib:${LD_LIBRARY_PATH}"


# Fix dbus error
# http://www.torkwrench.com/2011/12/16/d-bus-library-appears-to-be-incorrectly-set-up-failed-to-read-machine-uuid-failed-to-open-varlibdbusmachine-id/
RUN dbus-uuidgen > /var/lib/dbus/machine-id

# VFX Platform
ENV VFXPLATFORM 2017

# Enable additional output from Qt.py
ENV QT_VERBOSE true
ENV QT_TESTING true

# Xvfb
ENV DISPLAY :99

# Prevent error: "Qt: Failed to create XKB context!"
# https://lists.debian.org/debian-backports/2014/10/msg00061.html
ENV QT_XKB_CONFIG_ROOT=/usr/share/X11/xkb

# Warnings are exceptions
ENV PYTHONWARNINGS="ignore"


WORKDIR /workdir/Qt.py

# Put chmod command in here, in case we change the entrypoint in the future using
# docker run --entrypoint=...
ENTRYPOINT cp -r /Qt.py /workdir && chmod +x entrypoint.sh && ./entrypoint.sh
