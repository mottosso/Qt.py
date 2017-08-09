#!/bin/bash
set -e

# Python versions are defined in the Dockerfile
python_versions=( ${PYTHON_VER} ${PYTHON3_VER} )

# For each Python version, perform tests
for TEST_PY_VER in "${python_versions[@]}"; do

    echo "Running Python ${TEST_PY_VER} tests.."
    export NOSETESTS_BINARY=nosetests${TEST_PY_VER}

    echo "#\n# Testing implementation.."
        python${TEST_PY_VER} -u run_tests.py
    echo "#\n# Testing caveats..\n#"
        python${TEST_PY_VER} build_caveats.py
        nosetests${TEST_PY_VER} \
            --verbose \
            --with-doctest \
            --with-process-isolation \
            test_caveats.py
    echo "#\n# Testing membership..\n#"
        python${TEST_PY_VER} build_membership.py
        nosetests${TEST_PY_VER} \
            --verbose \
            test_membership.py
    echo "#\n# Testing examples..\n#"
        nosetests${TEST_PY_VER} \
            --verbose \
            --with-process-isolation \
            --with-doctest \
            --exe \
                examples/*/*.py

done

echo Done
