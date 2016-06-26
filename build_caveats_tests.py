"""Caveats do as advertised"""


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
            if line.startswith("#### "):
                current_header = line.rstrip()
            if line.startswith("```"):
                in_block = False
            if in_block:
                current_block.append(line)
            if line.startswith("```python"):
                in_block = True
                current_block = list()
                current_block.append(current_header)
                blocks.append(current_block)

    return list({
        "header": block[0].strip("# ")         # Remove Markdown
                          .rstrip()            # Remove newline
                          .lower()             # PEP08
                          .replace(" ", "_")   # Only allow spaces..
                          .replace(".", "_"),  # ..and dots in headers.
        "binding": block[1].strip("# ")
                           .rstrip(),
        "body": block[2:]
    } for block in blocks)


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

        block["header"] = block["header"] + str(function_count)
        block["body"] = "    ".join(block["body"])

        tests.append("""\

def test_{header}():
    '''Test {header}

    >>> from nose.tools import assert_raises
    >>> import os
    >>> os.environ["QT_PREFERRED_BINDING"] = "{binding}"
    {body}
    '''

    """.format(**block))

    with open("test_caveats.py", "w") as f:
        f.write("".join(tests))
