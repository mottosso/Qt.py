import io
import re


def parse(fname):
    """Return blocks of code as list of dicts

    Arguments:
        fname (str): Relative name of caveats file

    """

    blocks = []
    with io.open(fname, "r", encoding="utf-8") as f:
        in_block = False
        current_block = None
        current_header = ""

        for line in f:
            # Doctests are within a quadruple hashtag header.
            if line.startswith("#### "):
                current_header = line.rstrip()

            # The actuat test is within a fenced block.
            if line.startswith("```"):
                in_block = False

            if in_block:
                current_block.append(line)

            if line.startswith("```python"):
                in_block = True
                current_block = []
                current_block.append(current_header)
                blocks.append(current_block)

    tests = []
    for block in blocks:
        header = (
            block[0]
            .strip("# ")  # Remove Markdown
            .rstrip()  # Remove newline
            .lower()  # PEP08
        )

        # Remove unsupported characters
        header = re.sub(r"\W", "_", header)

        # Adding "untested" anywhere in the first line of
        # the doctest excludes it from the test.
        if "untested" in block[1].lower():
            continue

        # The first line may list multiple bindings, e.g. `# PySide2, PyQt5`,
        # the test will be skipped if the tox env is not testing those bindings
        bindings = re.sub(" ", "", block[1])  # Remove spaces
        bindings = (
            bindings.strip("#")
            .rstrip()  # Remove newline
            .split(",")
        )

        # Adding "qapp" creates a QApplication before the example runs (if needed)
        # and exits it afterward, for examples that need one. Note that after the
        # first qapp is created in a process you need to use `instance()` instead.
        needs_qapp = "qapp" in bindings
        if needs_qapp:
            bindings = [b for b in bindings if b != "qapp"]

        tests.append(
            {
                "header": header,
                "bindings": bindings or [None],
                "body": block[2:],
                "needs_qapp": needs_qapp,
            }
        )

    return tests


# The generated test functions don't have body, only a docstring. Unfortunately
# we can't use `nose ... --with-doctest` as it seems to require test discovery
# that complicates the testing setup. The tests would end up not running any code
# and always pass successfully. Instead we make each test call the `_run_doctest`
# function to ensure the test is actually run.
PREAMBLE = """\
import os
import unittest
import doctest


def binding():
    return os.environ.get("QT_PREFERRED_BINDING")


def _run_doctest(func, name):
    finder = doctest.DocTestFinder()
    # Enable doctest support for "..." in test output to handle wildcard text.
    runner = doctest.DocTestRunner(optionflags=doctest.ELLIPSIS)
    failures = tries = 0
    for test in finder.find(func, name, globs=globals()):
        f, t = runner.run(test)
        failures += f
        tries += t
    if failures:
        raise AssertionError(f"{failures} of {tries} doctest statements failed")
"""


FUNCTION_DEF = '''\

{decorator}def test_{count}_{header}():
    """Test {header}

    >>> import os, sys
    >>> _ = os.environ.pop("QT_VERBOSE", None)  # Disable debug output
    {body}
    """
    _run_doctest(
        test_{count}_{header},
        "test_{count}_{header}",
    )
'''


def format_(blocks):
    """Produce Python module from blocks of tests

    Arguments:
        blocks (list): Blocks of tests from func:`parse()`

    """

    tests = [PREAMBLE]
    function_count = 0  # For each test to have a unique name

    for block in blocks:
        # Validate docstring format of body
        if not any(line[:3] == ">>>" for line in block["body"]):
            # A doctest requires at least one `>>>` directive.
            block["body"].insert(
                0, ">>> assert False, 'Body must be in docstring format'\n"
            )

        # Validate the binding(s) on the first line
        valid_binding = all(
            b in ("PySide2", "PySide6", "PyQt6", "PyQt5") for b in block["bindings"]
        )
        if not valid_binding:
            block["body"].insert(0, ">>> assert False, 'Invalid binding'\n")

        if block["needs_qapp"]:
            block["body"].append(">>> _app.exit()\n")
            block["body"].insert(
                0,
                ">>> _app = _QtWidgets.QApplication.instance() or "
                "_QtWidgets.QApplication(sys.argv)\n",
            )
            block["body"].insert(0, ">>> from Qt import QtWidgets as _QtWidgets\n")

        function_count += 1
        block["count"] = str(function_count)
        block["body"] = "    ".join(block["body"])
        # The caveat tests are written to only run for the bindings they were
        # written for (using the binding comment). We use separate tox envs
        # to specifically test a target binding, so trying to run tests not
        # written for that binding may error out incorrectly.
        block["decorator"] = (
            ""
            if not valid_binding
            else (
                "@unittest.skipUnless(\n"
                f"    binding() in {tuple(block['bindings'])!r},\n"
                '    f"{binding()} is being tested but test targets: '
                f'{", ".join(block["bindings"])}",\n'
                ")\n"
            )
        )
        tests.append(FUNCTION_DEF.format(**block))

    return tests
