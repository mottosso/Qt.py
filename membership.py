import os
import re
import pkgutil
import json
import platform
from argparse import ArgumentParser
from functools import reduce
from pprint import pprint
from pathlib import Path


MEMBERSHIP_PATH = Path("./.members")

SKIP_MODULES = [
    "PyQt5.Qt",  # This module only exists in PyQt5 and is not exposed by Qt.py
    "PyQt5.uic.pyuic",  # Problematic as it is executed on import
    # These modules are only available on windows
    "PyQt5.QAxContainer",
    "PyQt6.QAxContainer",
    "PySide2.QtAxContainer",
    "PySide6.QtAxContainer",
]
SKIP_MEMBERS = [
    "QIntList",  # Missing from Qt5 or PyQt6, but present in ~50 modules
    "qApp",  # See main README.md on qApp
    "QWinEventNotifier",  # This class is only available on Windows.
]

# Will contain all modules for the current binding
MODULES = []

# Flags from environment variables
QT_VERBOSE = bool(os.getenv("QT_VERBOSE"))

# Names of bindings for major Qt versions
BINDING_NAMES_QT5 = ["PySide2", "PyQt5"]
BINDING_NAMES_QT6 = ["PySide6", "PyQt6"]

# Include these module names in common modules even if they have no common
# members. They will be assigned using the misplaced members.
MISPLACED_MODULES = [
    "QtOpenGL",
]


def read_json(filename):
    """Read JSON, return dict"""

    with filename.open("r") as data_file:
        return json.load(data_file)


def write_json(dictionary, filename):
    """Write dictionary to JSON"""
    filename.parent.mkdir(exist_ok=True)
    with filename.open("w") as data_file:
        json.dump(dictionary, data_file, indent=4, sort_keys=True)
    print("--> Wrote " + filename.name)


def write_markdown_row(file_obj, row, cls_width=0):
    """Writes a compact markdown table row. This works around a maximum
    character limit in github wiki markdown rendering.

    Use minimal white space while maintaining readability to prevent
    exceeding the apparent maximum markdown text length for github markdown
    rendering. This appears to be 512,000 characters. The headers are
    oversized but the data columns remain readable.
    """
    for i, cell in enumerate(row):
        if i == 0:
            cell = f"{cell: <{cls_width}}"
        file_obj.write(f"| {cell} ")
    file_obj.write("|\n")


def write_markdown_tables(rows, filename, headers):
    """Generate a text file that's easy to read and supported by github markdown"""

    module_exists = "_module exists_"
    # Make the rendered column width smaller by wrapping header text
    headers = [h.replace("-", " ", 1).replace("_", " ") for h in headers]
    # Remove the Module column, each module will have its own table.
    headers = headers[1:]

    classes = {}
    for row in rows:
        classes.setdefault(row[0], []).append(row[1:])

    with filename.open("w") as data_file:
        # Build a table for each module in its own section
        for module, rows in classes.items():
            data_file.write(f"# {module}\n\n")
            write_markdown_row(data_file, headers)
            write_markdown_row(data_file, ["---" for _ in headers])

            # Make the class column to the max width of the table
            cls_width = max([len(row[0]) for row in rows] + [len(module_exists)])

            for row in rows:
                if not row[0]:
                    # The blank row at the start indicates if the module exists
                    row[0] = module_exists
                    row[-1] = ""
                else:
                    # Show any uses of this class name in other modules
                    duplicates = sorted(row[-1])
                    duplicates.remove(module)
                    if len(duplicates) > 5:
                        duplicates = [f"Present in {len(duplicates)} modules"]
                    row[-1] = ", ".join(duplicates)

                write_markdown_row(data_file, row, cls_width)
            data_file.write("\n")
    print("--> Wrote " + filename.name)


def compare(dicts):
    """Combine the contents of a dict of multiple Qt bindings member mappings.

    Returns a two item dictionary where "bindings" is a list of all binding names
    given this method and "members" is the all Qt mappings common across all bindings.
    """

    ret = {
        # Store the binding names this dict was generated from
        "bindings": sorted(dicts.keys()),
        "members": {},
    }

    if not dicts:
        return ret

    common_members = ret["members"]
    common_keys = reduce(lambda x, y: x & y, map(dict.keys, dicts.values()))
    for k in common_keys:
        # Sort the lists here so they are stored consistently in the json later
        members = sorted(
            reduce(lambda x, y: x & y, [set(d[k]) for d in dicts.values()])
        )
        # Only add modules which have common members
        if members:
            common_members[k] = members

    # Add empty misplaced modules. These are where we will add misplaced members
    # for modules that are not common
    for module in MISPLACED_MODULES:
        if module not in common_members:
            common_members[module] = []

    return ret


def membership_table(binding_maps):
    rows = {}
    headers = (
        ["Module", "Class"] + list(binding_maps.keys()) + ["Potentially Misplaced"]
    )
    columns = len(binding_maps) + 1
    cls_modules = {}

    def add_item(module_name, member, column):
        if member:
            member_id = f"{module_name}:{member}"
        else:
            member_id = module_name
        if member_id not in rows:
            # Create row if not already existing
            rows[member_id] = [module_name, member] + [" "] * columns
        # Add a X for the binding column
        rows[member_id][column] = "X"

        if member:
            # Keep track of any other modules that expose a class with the same
            # name. This is useful for determining if the module was moved.
            # Ie. Misplaced Members
            cls_module = cls_modules.setdefault(member, set())
            # Note: This set instance is shared across all members with the same
            # name so any future uses will show up in all previous instances.
            cls_module.add(module_name)
            rows[member_id][-1] = cls_module

    for binding, classes in binding_maps.items():
        column = headers.index(binding)
        for module_name in classes:
            # Add a row for each module
            add_item(module_name, "", column)
            # Add a row for each class
            for member in classes[module_name]:
                add_item(module_name, member, column)

    return rows, headers


def members_for_binding_names(binding_names, memberships):
    """Filter memberships by a list of Qt binding names.

    The binding_names are the start of the membership dictionary keys.
    """
    ret = {}
    for binding in memberships:
        for name in binding_names:
            if binding.startswith(name):
                ret[binding] = memberships[binding]
    return ret


def clean_common_members():
    """Remove the temporary .json files generated by this script."""
    if not MEMBERSHIP_PATH.exists():
        return
    for f in MEMBERSHIP_PATH.iterdir():
        if f.suffix not in (".json", ".md"):
            continue
        print(f"--> Removing membership file: {f}")
        f.unlink()


def write_member_files(memberships, json_name=None, markdown_name=None):
    """Write the various files showing Qt binding membership.

    The table files contain a row for each member. A column is added for each
    Qt binding with a X if that binding implements that member.

    Args:
        memberships: A dict of binding memberships loaded from the .json files
            created for each QT binding.
        json_name: Contains the members common to all provided memberships.
        markdown_name: Table of members formatted to be easily human readable and
            supported by github markdown.
    """
    if json_name:
        filename = MEMBERSHIP_PATH / json_name
        common_members = compare(memberships)
        write_json(common_members, filename)

    members, headers = membership_table(memberships)
    members = sorted(members.values())

    if markdown_name:
        filename = MEMBERSHIP_PATH / markdown_name
        write_markdown_tables(members, filename, headers)


def sort_qt_file(path):
    """Sort a Qt filename consistently by major/minor qt and python version.

    Note: It is preferred to use `reverse=True` when sorting with this method.
    """
    name = path.stem
    match = re.match(
        r"(?P<qt>(?P<binding>PyQt|PySide)\d)-(?P<qt_ver>[\d.]+)"
        r"_py-(?P<py_ver>[\d.]+)",
        name,
    )
    if not match:
        raise ValueError(f"Invalid qt name: {path}")

    qt_name = match.group("qt")
    if "6" in qt_name:
        qt_major = 6
    elif "5" in qt_name or "2" in qt_name:
        qt_major = 5
    else:
        qt_major = 4
    # Note: Sort PyQt after PySide
    binding = match.group("binding")  # .replace("PyQt", "Py_Qt")

    qt_ver = [int(x) for x in match.group("qt_ver").split(".")]
    py_ver = [int(x) for x in match.group("py_ver").split(".")]

    return qt_major, binding, qt_ver, py_ver


def generate_common_members():
    """Generate files with commonly shared members"""

    memberships = {}
    files = MEMBERSHIP_PATH.glob("Py*.*_py-*.json")
    for f in sorted(files, key=sort_qt_file, reverse=True):
        memberships[f.stem] = read_json(f)

    # Generate a mapping of all common members
    write_member_files(memberships, "common_members.json", "members.md")

    # Generate a mapping of all common Qt5 members
    qt5_common = members_for_binding_names(BINDING_NAMES_QT5, memberships)
    if qt5_common:
        write_member_files(qt5_common, "common_members_qt5.json", "members_qt5.md")

    # Generate a mapping of all common Qt6 members
    qt6_common = members_for_binding_names(BINDING_NAMES_QT6, memberships)
    if qt6_common:
        write_member_files(qt6_common, "common_members_qt6.json", "members_qt6.md")


if __name__ == "__main__":
    # Parse command line arguments
    parser = ArgumentParser(
        description="Gather and report on Qt binding common members."
    )
    parser.add_argument(
        "--binding", help="Generate for this Qt binding. Example: PySide6"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove all files generated by this command.",
    )
    parser.add_argument(
        "--generate-common-members",
        action="store_true",
        dest="generate",
        help="Combine generated bindings into common_members",
    )

    args = parser.parse_args()

    if args.clean:
        clean_common_members()
    if args.generate:
        generate_common_members()
    elif args.binding:
        # Import <binding>
        binding = __import__(args.binding)

        for _, modname, _ in pkgutil.walk_packages(
            path=binding.__path__, prefix=binding.__name__ + ".", onerror=lambda x: None
        ):
            if modname not in SKIP_MODULES:
                MODULES.append(modname)
                basemodule = modname[: modname.rfind(".")]
                submodule = modname[modname.rfind(".") + 1 :]
                try:
                    import_statement = "from " + basemodule + " import " + submodule
                    exec(import_statement)
                except (ImportError, AttributeError, SyntaxError) as error:
                    # SyntaxError catched here because e.g. _port3
                    # running on Python 2...
                    print("WARNING: Skipped import", modname, error)

                try:
                    raw_members = []  # avoid Hound errors
                    exec("raw_members = dir(" + submodule + ")")
                    members = []
                    for member in raw_members:
                        if member not in SKIP_MEMBERS and not member.startswith("_"):
                            try:
                                import_statement = (
                                    "from "
                                    + basemodule
                                    + "."
                                    + submodule
                                    + " import "
                                    + member
                                )
                                exec(import_statement)
                                # print(import_statement)
                                MODULES.append(modname + "." + member)
                            except (AttributeError, SyntaxError) as error:
                                # SyntaxError catched here because e.g. _port3
                                # running on Python 2...
                                print("WARNING: Skipped import", modname, error)
                except NameError as error:
                    print("WARNING: Skipped dir() command", modname, error)

        # Remove duplicates and sort
        MODULES = sorted(set(MODULES))

        if QT_VERBOSE:
            # Print all modules (for debugging)
            for module in MODULES:
                print(module)

        # Create dictionary
        members = {}
        for module in MODULES:
            key = module.split(".")[1]
            if key not in members:
                members[key] = []
            try:
                value = module.split(".")[2]
                members[key].append(value)
            except IndexError:
                pass

        # Sort and remove duplicates
        sorted_members = {}
        for key, value in members.copy().items():
            sorted_members[key] = sorted(set(value))

        if QT_VERBOSE:
            # Debug
            pprint(sorted_members)

        # Write to disk in the .members folder with python and Qt version info.
        if "PySide" in args.binding:
            qtver = binding.__version__
        else:
            qtver = binding.QtCore.PYQT_VERSION_STR
        pyver = platform.python_version()
        filepath = MEMBERSHIP_PATH / f"{binding.__name__}-{qtver}_py-{pyver}.json"
        write_json(sorted_members, filepath)
