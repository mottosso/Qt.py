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
        "nosetests",
        "--verbose",
        "--with-process-isolation",
        "--exe",
    ]

    argv.extend(sys.argv[1:])

    # Running each test independently via subprocess
    # enables tests to filter out from tests.py before
    # being split into individual processes via the
    # --with-process-isolation feature of nose.
    with binding("PyQt4"):
        subprocess.call(argv)

    with binding("PySide"):
        subprocess.call(argv)

    with binding("PyQt5"):
        subprocess.call(argv)

    with binding("PySide2"):
        argv.append("--with-doctest")  # Run doctests once
        subprocess.call(argv)
