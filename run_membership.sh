#!/bin/bash

# Exit with non-zero code if errors in script
set -e

array=( PySide PySide2 PyQt4 PyQt5 )
for binding in "${array[@]}"
do
    docker run -ti --rm -v $(pwd):/Qt.py --entrypoint="python2.7" fredrikaverpil/qt.py:2017 /Qt.py/membership.py --binding=$binding
done
