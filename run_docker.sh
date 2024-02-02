#!/bin/bash

# docker run -ti --rm -v $(pwd):/Qt.py --entrypoint bash fredrikaverpil/qt.py:2017
docker run -ti --rm -v $(pwd):/Qt.py --entrypoint bash fredrikaverpil/qt.py:2018 -c "cp -r /Qt.py/* . && bash"
