#!/bin/bash

# Exit with non-zero code if errors in script
set -e

# Generate PySide.json, PySide2.json, PyQt4.json, PyQt5.json
array=( PySide PySide2 PyQt4 PyQt5 )
for binding in "${array[@]}"
do
    docker run -ti --rm -v $(pwd):/Qt.py --entrypoint="python2.7" fredrikaverpil/qt.py:2018 /Qt.py/membership.py --binding=$binding
done

# Rename QtGui key to QtWidgets
docker run -ti --rm -v $(pwd):/Qt.py --entrypoint="python3.5" fredrikaverpil/qt.py:2018 /Qt.py/membership.py --copy-qtgui

# Generate common_members.json
docker run -ti --rm -v $(pwd):/Qt.py --entrypoint="python3.5" fredrikaverpil/qt.py:2018 /Qt.py/membership.py --generate-common-members

# Sort common members
docker run -ti --rm -v $(pwd):/Qt.py --entrypoint="python3.5" fredrikaverpil/qt.py:2018 /Qt.py/membership.py --sort-common-members
