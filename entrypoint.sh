#!/bin/bash

# Exit with non-zero code if errors in script
set -e

# Start Xvfb
Xvfb :99 -screen 0 1024x768x16 2>/dev/null &
while ! ps aux | grep -q '[0]:00 Xvfb :99 -screen 0 1024x768x16'; do
    echo "Waiting for Xvfb..."
    sleep 1
done

printf "#\n# Running tests in Python ${PYTHON}\n"
export NOSETESTS_BINARY=nosetests${PYTHON}
printf "#\n# Testing implementation..\n"
    python${PYTHON} -u run_tests.py
printf "#\n# Testing caveats..\n"
    python${PYTHON} build_caveats.py
    nosetests${PYTHON} \
        --verbose \
        --with-doctest \
        --with-process-isolation \
        test_caveats.py
printf "#\n# Testing examples..\n"
    nosetests${PYTHON} \
    --verbose \
    --with-process-isolation \
    --with-doctest \
    --exe \
        examples/*/*.py

printf Done
