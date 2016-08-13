#!/bin/bash
#
# This build script installs PySide2 on Ubuntu 14.04-based system.
#
# dependencies:
# 	git
# 	cmake3
# 	wget
# 	freeglut3-dev
# 	qt55-meta-full (ppa:beineri/opt-qt551-trusty)
# 	libxslt-dev
#
# usage:
#   $ ./install_pyside2.sh

mkdir build
pushd build

# Build
git clone https://code.qt.io/pyside/pyside-setup
source /opt/qt55/bin/qt55-env.sh
python pyside-setup/setup.py install \
	--cmake=$/usr/local/bin/cmake \
	--qmake=$/opt/qt55/bin/qmake \
	--openssl=/usr/bin

# Teardown
popd
rm -rf build
