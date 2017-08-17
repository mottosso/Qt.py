import io
import re
import sys


def parse(fname):
    """Return blocks of code as list of dicts

    Arguments:
        fname (str): Relative name of caveats file

    """

    blocks = list()
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
                current_block = list()
                current_block.append(current_header)
                blocks.append(current_block)

    tests = list()
    for block in blocks:
        header = (
            block[0].strip("# ")  # Remove Markdown
                    .rstrip()     # Remove newline
                    .lower()      # PEP08
        )

        # Remove unsupported characters
        header = re.sub(r"\W", "_", header)

        # Adding "untested" anywhere in the first line of
        # the doctest excludes it from the test.
        if "untested" in block[1].lower():
            continue

        data = re.sub(" ", "", block[1])  # Remove spaces
        data = (
            data.strip("#")
                .rstrip()     # Remove newline
                .split(",")
        )

        binding, doctest_version = (data + [None])[:2]

        # Run tests on both Python 2 and 3, unless explicitly stated
        if doctest_version is not None:
            if doctest_version not in ("Python2", "Python3"):
                raise SyntaxError(
                    "Invalid Python version:\n%s\n"
                    "Python version must follow binding, e.g.\n"
                    "# PyQt5, Python3" % doctest_version)

            active_version = "Python%i" % sys.version_info[0]
            if doctest_version != active_version:
                continue

        tests.append({
            "header": header,
            "binding": binding,
            "body": block[2:]
        })

    return tests


def format_(blocks):
    """Produce Python module from blocks of tests

    Arguments:
        blocks (list): Blocks of tests from func:`parse()`

    """

    tests = list()
    function_count = 0  # For each test to have a unique name

    for block in blocks:

        # Validate docstring format of body
        if not any(line[:3] == ">>>" for line in block["body"]):
            # A doctest requires at least one `>>>` directive.
            block["body"].insert(0, ">>> assert False, "
                                 "'Body must be in docstring format'\n")

        # Validate binding on first line
        if not block["binding"] in ("PySide", "PySide2", "PyQt5", "PyQt4"):
            block["body"].insert(0, ">>> assert False, "
                                 "'Invalid binding'\n")

        if sys.version_info > (3, 4) and block["binding"] in ("PySide"):
            # Skip caveat test if it requires PySide on Python > 3.4
            continue
        else:
            function_count += 1
            block["header"] = block["header"]
            block["count"] = str(function_count)
            block["body"] = "    ".join(block["body"])
            tests.append("""\

def test_{count}_{header}():
    '''Test {header}

    >>> import os, sys
    >>> PYTHON = sys.version_info[0]
    >>> long = int if PYTHON == 3 else long
    >>> _ = os.environ.pop("QT_VERBOSE", None)  # Disable debug output
    >>> os.environ["QT_PREFERRED_BINDING"] = "{binding}"
    {body}
    '''

    """.format(**block))

    return tests
