#!/bin/bash

# Exit with non-zero code if errors in script
set -e

docker run -ti --rm -v $(pwd):/Qt.py --entrypoint="python2.7" fredrikaverpil/qt.py:2017 "/Qt.py/membership.py"
