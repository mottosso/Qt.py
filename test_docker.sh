#!/bin/bash

# Exit from bash shell script on error
set -e

docker run --rm -v $(pwd):/Qt.py -e PYTHON=2.7 fredrikaverpil/qt.py:2017
docker run --rm -v $(pwd):/Qt.py -e PYTHON=3.4 fredrikaverpil/qt.py:2017
docker run --rm -v $(pwd):/Qt.py -e PYTHON=3.5 fredrikaverpil/qt.py:2017

docker run --rm -v $(pwd):/Qt.py -e PYTHON=2.7 fredrikaverpil/qt.py:2018
docker run --rm -v $(pwd):/Qt.py -e PYTHON=3.4 fredrikaverpil/qt.py:2018
docker run --rm -v $(pwd):/Qt.py -e PYTHON=3.5 fredrikaverpil/qt.py:2018
docker run --rm -v $(pwd):/Qt.py -e PYTHON=3.6 fredrikaverpil/qt.py:2018
