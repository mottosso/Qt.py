#!/bin/bash

mkdir build
pushd build

wget http://sourceforge.net/projects/pyqt/files/sip/sip-4.17/sip-4.17.tar.gz
wget https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.5.1/PyQt-gpl-5.5.1.tar.gz

tar xzf sip-4.17.tar.gz
pushd sip-4.17
python configure.py && \
    make && \
    sudo make install
popd

tar xzf PyQt-gpl-5.5.1.tar.gz
pushd PyQt-gpl-5.5.1
python configure.py \
    --sip=/usr/bin/sip \
    --disable=QtPrintSupport \
    --qmake=/opt/qt55/bin/qmake \
    --confirm-license && \
    make -j 4 && \
    sudo make install
popd

popd
rm -rf build
