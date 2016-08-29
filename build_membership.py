import json

# Safe-guard against incomplete API
from PySide2 import __all__
__all__.remove("QtOpenGL")
__all__.remove("QtSql")
__all__.remove("QtSvg")

from PySide2 import *

# Serialise members
members = {}
for name, module in locals().copy().items():
    if name.startswith("_"):
        continue

    if name in ("json", "members"):
        continue

    members[name] = dir(module)

# Write to disk
with open("reference_members.json", "w") as f:
    json.dump(members, f, indent=4)


def build_test():
    header = """\
import os
import sys
import json

with open("reference_members.json") as f:
    reference_members = json.load(f)


"""

    test = """\
def test_{binding}_members():
    os.environ["QT_PREFERRED_BINDING"] = "{binding}"

    from Qt import *

    target_members = dict()
    for name, module in locals().copy().items():
        if name.startswith("_"):
            continue

        target_members[name] = dir(module)

    missing = dict()
    for module, members in reference_members.items():
        for member in members:
            if member not in target_members.get(module, []):
                if module not in missing:
                    missing[module] = []
                missing[module].append(member)

    message = ""
    for module, members in missing.items():
        message += "\\n%s: \\n - %s" % (module, "\\n - ".join(members))

    assert not missing, "{binding} is missing members: %s" % message

"""

    tests = list(test.format(binding=binding)
                 for binding in ["PyQt5",
                                 "PyQt4",
                                 "PySide"])

    with open("test_membership.py", "w") as f:
        contents = header + "\n".join(tests)
        print(contents)  # Preview content during tests
        f.write(contents)


if __name__ == '__main__':
    build_test()
