"""Caveats do as advertised"""

import re
import sys


def parse(fname):
    """Return blocks of code as list of dicts

    Arguments:
        fname (str): Relative name of caveats file

    """

    blocks = list()
    with open(fname) as f:
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
            block[0].strip("# ") # Remove Markdown
                    .rstrip()    # Remove newline
                    .lower()     # PEP08
        )

        # Remove unsupported characters
        header = re.sub(r"\W", "_", header)

        binding, doctest_version = (
            block[1].strip("# ")  # Remove previx
                    .rstrip()     # Remove newline
                    .split(",") +
            ["Python2"]  # Default
        )[:2]
        
        active_version = "Python%i" % sys.version_info[0]

        if doctest_version == active_version:
            tests.append({
                "header": header,
                "binding": binding,
                "body": block[2:]
            })

    return tests


if __name__ == '__main__':
    blocks = parse("CAVEATS.md")
    tests = list()
    function_count = 0  # For each test to have a unique name

    for block in blocks:
        function_count += 1

        # Validate docstring format of body
        if not any(line[:3] == ">>>" for line in block["body"]):
            # A doctest requires at least one `>>>` directive.
            block["body"].insert(0, ">>> assert False, "
                                 "'Body must be in docstring format'\n")

        # Validate binding on first line
        if not block["binding"] in ("PySide", "PySide2", "PyQt5", "PyQt4"):
            block["body"].insert(0, ">>> assert False, "
                                 "'Invalid binding'\n")

        block["header"] = block["header"]
        block["count"] = str(function_count)
        block["body"] = "    ".join(block["body"])

        tests.append("""\

def test_{count}_{header}():
    '''Test {header}

    >>> import os, sys
    >>> PY2 = sys.version_info[0] == 2
    >>> PY3 = sys.version_info[0] == 3
    >>> _ = os.environ.pop("QT_VERBOSE", None)  # Disable debug output
    >>> os.environ["QT_PREFERRED_BINDING"] = "{binding}"
    {body}
    '''

    """.format(**block))

    with open("test_caveats.py", "w") as f:
        f.write("".join(tests))
