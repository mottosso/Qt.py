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
    failures = []

    # Running each test independently via subprocess
    # enables tests to filter out from tests.py before
    # being split into individual processes via the
    # --with-process-isolation feature of nose.
    with binding("PyQt4"):
        _errors = subprocess.call(argv)
        errors += _errors
        if _errors:
            failures.append(os.environ["QT_PREFERRED_BINDING"])

    if sys.version_info <= (3, 4):
        with binding("PySide"):
            _errors = subprocess.call(argv)
            errors += _errors
            if _errors:
                failures.append(os.environ["QT_PREFERRED_BINDING"])

    with binding("PyQt5"):
        _errors = subprocess.call(argv)
        errors += _errors
        if _errors:
            failures.append(os.environ["QT_PREFERRED_BINDING"])

    with binding("PySide2"):
        _errors = subprocess.call(argv)
        errors += _errors
        if _errors:
            failures.append(os.environ["QT_PREFERRED_BINDING"])

    if errors:
        raise Exception(
            "{} binding(s) failed for {}.".format(errors, ", ".join(failures))
        )
