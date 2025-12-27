"""Tool to convert short form Qt enums to fully qualified enums in python code.

This script uses PySide2 to build a mapping between short enums and their fully
qualified enums. It scans a directory of .py files and converts any uses of the
short form into the fully qualified enum. PySide2 must be importable.

Show how many times a given short enum will be replaced for each file:
    python3 enum_converter.py /path/to/source/code

Add the `--write` argument to actually modify the files. This does not make
backups of the files changed.

Note: This file can be omitted when vendoring Qt.py.
"""

import argparse
import enum
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional


def qt_for_binding(binding):
    """Import Qt module with the requested binding."""
    os.environ["QT_PREFERRED_BINDING"] = binding
    if "QT_PREFERRED_BINDING_JSON" in os.environ:
        del os.environ["QT_PREFERRED_BINDING_JSON"]
    # To be able to capture stdout as json data we don't want Qt.py to
    # print to stdout, disable verbose mode.
    if "QT_VERBOSE" in os.environ:
        del os.environ["QT_VERBOSE"]

    import Qt

    return Qt


class QtEnumConverter:
    DEFAULT_IGNORED = ".tox,.eggs,build,dist"

    def __init__(self, verbosity=0, ignored: str = DEFAULT_IGNORED):
        self.ignored = ignored.split(",")
        self.Qt = qt_for_binding("PySide2")
        self.modules_not_loaded = set()

        # Unsure how to import these class types, so get them from objects
        self.enum_type = type(self.Qt.QtCore.Qt.AlignmentFlag)
        self.object_type = type(self.Qt.QtCore.Qt)
        self.verbosity = verbosity

        # The mapping of short to fully qualified enum names. Used to
        # update python scripts.
        self.enum_map: dict[str, str] = {}
        self.partial_enum: Optional[re.Pattern] = None
        # Module level view of all the enums also used to check for naming
        # conflicts where the short name maps to multiple long names.
        self.enum_module: dict[str, dict[str, list[str]]] = {}

    def enums_for_class(self, cls):
        """Include enums for a specific class."""
        module_name = cls.__module__.split(".")[-1]

        # Build a set of all enum classes on cls. These are the fully qualified
        # enum objects containing each individual enum value.
        enum_classes = set()
        for name in dir(cls):
            obj = getattr(cls, name)
            if isinstance(obj, self.enum_type):
                enum_classes.add(obj)

        # Find all short name enums on the class and map them to the fully
        # qualified enum name.
        enum_classes = tuple(enum_classes)
        for name in dir(cls):
            obj = getattr(cls, name)
            if isinstance(obj, enum_classes):
                short_name = f"{cls.__name__}.{name}"
                enum_name = str(obj).split(".", 3)[-1]
                full_name = f"{cls.__name__}.{enum_name}"
                self.enum_map[short_name] = full_name
                self.enum_module.setdefault(module_name, {}).setdefault(
                    short_name, []
                ).append(full_name)

    def enums_for_module(self, module):
        """Include enums for all classes in this module."""
        for cls_name in dir(module):
            cls = getattr(module, cls_name)
            if isinstance(cls, self.object_type):
                self.enums_for_class(cls)

    def enums_for_qt_py(self):
        """Include enums for common members of Qt.py."""
        for module_name in self.Qt._common_members:
            if not hasattr(self.Qt, module_name):
                self.modules_not_loaded.add(module_name)
                print(f"Module not loaded: {module_name}", file=sys.stderr)
                continue
            module = getattr(self.Qt, module_name)
            self.enums_for_module(module)

    def convert_enums_in_file(self, filepath: Path, root: Path, dry_run: bool) -> int:
        """Convert the enums in the given file.

        Based on https://stackoverflow.com/a/72658216 by Kristof Mulier
        """
        if not self.enum_map:
            self.enums_for_qt_py()

        # Read the content
        content = ""
        with filepath.open("r", encoding="utf-8", newline="\n", errors="replace") as f:
            content = f.read()

        changes = 0
        # Loop over all the keys in 'self.enum_map'. Perform a replacement in the
        # 'content' for each of them.
        for k, v in self.enum_map.items():
            if k not in content:
                continue
            # Compile a regex pattern that only looks for the old enum (represented
            # by the key of 'self.enum_map') if it is surrounded by bounds. What we
            # want to avoid is a situation like this:
            #     k = 'Qt.Window'
            #     k found in 'qt.Qt.WindowType.Window'
            # In the situation above, k is found in 'qt.Qt.WindowType.Window' such
            # that a replacement will take place there, messing up the code! By
            # surrounding k with bounds in the regex pattern, this won't happen.
            p = re.compile(rf"\b{k}\b")

            # Substitute all occurrences of k (key) in 'content' with v (value). The
            # 'subn()' method returns a tuple (new_string, number_of_subs_made).
            new_content, n = p.subn(v, content)
            if n == 0:
                assert new_content == content
                continue
            assert new_content != content
            relative_path = filepath.relative_to(root)
            q = "'"
            print(f"{q}{relative_path}{q}: Replace {q}{k}{q} => {q}{v}{q} ({n})")
            content = new_content
            # Record the number of enums updated in this file
            changes += n

        if dry_run:
            return changes

        with filepath.open("w", encoding="utf-8", newline="\n", errors="replace") as f:
            f.write(content)
        return changes

    def find_partials(self, filepath: Path, root: Path) -> int:
        """Find and report potential partial Enum uses

        We can't automatically replace them as this has a high likelihood of
        false positives.
        """
        if not self.enum_map:
            self.enums_for_qt_py()

        if not self.partial_enum:
            enums = {v.split(".")[-1] for v in self.enum_map.values()}
            self.partial_enum = re.compile(rf"\.({'|'.join(enums)})(?!\w)")

        # Read the content
        with filepath.open("r", encoding="utf-8", newline="\n", errors="replace") as f:
            content = f.readlines()

        changes = 0
        relative = filepath.relative_to(root)
        for ln, line in enumerate(content):
            clean_line = line.rstrip()
            matches = set()
            for v in self.enum_map.values():
                clean_line = clean_line.replace(v, "")

            for match in self.partial_enum.findall(clean_line):
                matches.add(match)
            if matches:
                if self.verbosity >= 0:
                    print(
                        f'File: "{relative}", line:{ln + 1}, for {", ".join(matches)}'
                    )
                if self.verbosity >= 1:
                    print(f"    {line.strip()}")
                changes += 1

        return changes

    def convert_all(self, directory: Path, dry_run: bool, partial: bool = False) -> int:
        """Search and replace all enums."""
        ignored = [directory / i for i in self.ignored]
        changes = 0
        # Using os.walk instead of pathlib's walk to support older python's
        for _root, _, files in os.walk(directory):
            root = Path(_root)
            skip = False
            for ignore in ignored:
                if root == ignore:
                    skip = True
                    break
                # `pathlib.Path.is_relative_to` was added in python 3.9
                if ignore == root or ignore in root.parents:
                    skip = True
                    break
            if skip:
                if self.verbosity >= 1:
                    print(f"Ignoring: {root}", file=sys.stderr)
                continue
            for f in files:
                filepath = root / f
                if filepath.suffix != ".py":
                    continue
                if self.verbosity >= 2:
                    print(f"Checking: {filepath}")
                if partial:
                    changes += self.find_partials(filepath, directory)
                else:
                    changes += self.convert_enums_in_file(filepath, directory, dry_run)

        return changes


class DuplicateEnums:
    """Find all Qt6 enums that have duplicate short names using PySide6."""

    def __init__(self, binding="PySide6"):
        self.Qt = qt_for_binding(binding)

    def enums_for_module(self, module):
        """Include enums for all classes in this module."""
        cls_map = {}
        for cls_name in dir(module):
            cls = getattr(module, cls_name)
            enum_map = {}
            for name in dir(cls):
                try:
                    obj = getattr(cls, name)
                except AttributeError:
                    pass
                if isinstance(obj, enum.EnumMeta):
                    for e in obj:
                        # Store the name and value of each enum
                        enum_name = f"{name}.{e.name}"
                        value = f"{enum_name}, {e.value}"
                        enum_map.setdefault(e.name, []).append(value)

            # Add to cls_map only if a duplicate short enum name is found.
            dupe_map = {k: e for k, e in enum_map.items() if len(e) > 1}
            if dupe_map:
                cls_map.setdefault(cls_name, {}).update(dupe_map)

        return cls_map

    def enums_for_qt_py(self):
        """Include enums for common members of Qt.py."""
        ret = {}
        for module_name in self.Qt._common_members:
            if not hasattr(self.Qt, module_name):
                print(f"Module not loaded: {module_name}", file=sys.stderr)
                continue
            module = getattr(self.Qt, f"_{module_name}")
            enums = self.enums_for_module(module)
            if enums:
                ret[module_name] = enums
        return ret


def parse_args():
    parser = argparse.ArgumentParser(
        "Convert Qt5 enums to fully qualified enums for Qt6 compliance."
    )
    parser.add_argument(
        "-w",
        "--write",
        action="store_true",
        help="Write changes to the files. This does not create backups",
    )
    parser.add_argument(
        "--ignored",
        default=QtEnumConverter.DEFAULT_IGNORED,
        help="A comma separated list of relative file paths to ignore. "
        f"Defaults to: {QtEnumConverter.DEFAULT_IGNORED}",
    )
    parser.add_argument(
        "--show",
        choices=["map", "modules", "dups"],
        help="Print enum mappings as json. map: shows the mapping of short to "
        "fully qualified enums used to convert. modules: shows that mapping "
        "including the module it belongs to. dups: shows enums in PySide6 that "
        "have duplicate names on the same class causing ambiguity with short "
        "names. dups requires PySide6 and the others require PySide2 installed.",
    )
    parser.add_argument(
        "--partial",
        action="store_true",
        help="Report any potential enum uses that can not be automatically fixed. "
        "This can happen if the code accesses enums from the instance instead of "
        "directly from the class name.",
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        action="count",
        default=0,
        help="Increase the verbosity of the output.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="count",
        default=0,
        help="Decrease the verbosity of the output.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="The Return Code becomes the number of enums that were/require "
        "changing. Can be used with --write. Use this to check for enum use "
        "regression.",
    )
    parser.add_argument(
        "target", type=Path, nargs="?", help="Directory to process recursively"
    )

    return parser.parse_args()


def add_binding_info(data, qt, modules_not_loaded=None):
    """Adds info on the PySide version used to generate this dict.

    Uses the name BINDING_INFO, etc as this normally gets sorted to the top of
    the json output when using `sort_keys`.
    """
    data["BINDING_INFO"] = f"{qt.__binding__}=={qt.__binding_version__}"
    # Add lists of modules that could not be imported
    if modules_not_loaded:
        data["MODULES_NOT_LOADED"] = sorted(modules_not_loaded)


if __name__ == "__main__":
    args = parse_args()

    # Merge the quiet and verbosity arguments
    args.verbosity -= args.quiet

    if args.show == "dups":
        # Show duplicate enum short names found in PySide6
        checker = DuplicateEnums()
        dups = checker.enums_for_qt_py()
        add_binding_info(dups, checker.Qt)
        print(json.dumps(dups, indent=4, sort_keys=True))
        sys.exit()

    mapper = QtEnumConverter(verbosity=args.verbosity, ignored=args.ignored)
    mapper.enums_for_qt_py()

    if args.show:
        # Show the conversion information gathered from PySide2
        if args.show == "map":
            mappings = mapper.enum_map
        else:
            mappings = mapper.enum_module  # type: ignore[assignment]
        add_binding_info(mappings, mapper.Qt, mapper.modules_not_loaded)
        print(json.dumps(mappings, indent=4, sort_keys=True))
    else:
        # Search .py files and update to fully qualified enum names
        changes = mapper.convert_all(
            args.target, dry_run=not args.write, partial=args.partial
        )

        # Report the number of enum changes
        if args.partial:
            print(f"{changes} partial enums found.")
        elif args.write:
            print(f"{changes} enums changed.")
        else:
            print(f"{changes} enums require changes.")
        # Set the return code to the number of enums being changed if enabled
        if args.check:
            sys.exit(changes)
