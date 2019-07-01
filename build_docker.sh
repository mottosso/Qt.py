#!/bin/bash

# Exit from bash shell script on error
set -e

docker build . -f Dockerfile.vfxplatform2017 -t fredrikaverpil/qt.py:2017
docker build . -f Dockerfile.vfxplatform2018 -t fredrikaverpil/qt.py:2018
