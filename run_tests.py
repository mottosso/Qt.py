import os
import sys
import contextlib
import subprocess


@contextlib.contextmanager
def binding(binding):
    """Prepare an environment for a specific binding"""

    sys.stderr.write("""\
#
# Running tests with %s..
#
""" % binding)

    os.environ["QT_PREFERRED_BINDING"] = binding

    try:
        yield
    except:
        pass

    os.environ.pop("QT_PREFERRED_BINDING")


if __name__ == "__main__":

    argv = [
        os.environ.get('NOSETESTS_BINARY'),
        "--verbose",
        "--with-process-isolation",
        "--exe",
    ]

    errors = 0

    # Running each test independently via subprocess
    # enables tests to filter out from tests.py before
    # being split into individual processes via the
    # --with-process-isolation feature of nose.
    with binding("PyQt4"):
        errors += subprocess.call(argv)

    if sys.version_info <= (3, 4):
        with binding("PySide"):
            errors += subprocess.call(argv)

    with binding("PyQt5"):
        errors += subprocess.call(argv)

    with binding("PySide2"):
        errors += subprocess.call(argv)

    if errors:
        raise Exception("%i binding(s) failed." % errors)
