#!/bin/bash

wget http://www.cmake.org/files/v3.2/cmake-3.2.2.tar.gz
tar xf cmake-3.2.2.tar.gz
pushd cmake-3.2.2

./configure
make -j4
make install

popd
rm -rf cmake-3.2.2
