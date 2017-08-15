#!/bin/bash

cp -r /Qt.py /workdir
Xvfb :99 -screen 0 1024x768x16 2>/dev/null &
while ! ps aux | grep -q '[0]:00 Xvfb :99 -screen 0 1024x768x16';
    do echo "Waiting for Xvfb..."; sleep 1; done

echo "#\n# Running tests in Python ${PYTHON}"
export NOSETESTS_BINARY=nosetests${PYTHON}

echo "#\n# Testing implementation.."
    python${PYTHON} -u run_tests.py
echo "#\n# Testing caveats..\n#"
    python${PYTHON} build_caveats.py
    nosetests${PYTHON} \
        --verbose \
        --with-doctest \
        --with-process-isolation \
        test_caveats.py
echo "#\n# Testing membership..\n#"
    python${PYTHON} build_membership.py
    nosetests${PYTHON} \
        --verbose \
        test_membership.py
echo "#\n# Testing examples..\n#"
    nosetests${PYTHON} \
    --verbose \
    --with-process-isolation \
    --with-doctest \
    --exe \
        examples/*/*.py
echo Done
