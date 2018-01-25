import os
import pkgutil
import json
from optparse import OptionParser
from functools import reduce
from pprint import pprint


# This is where all files are read from and saved to
PREFIX = '/Qt.py'


SKIP_MODULES = [
    'PyQt4.uic.pyuic',  # Problematic as it is executed on import
    'PyQt5.uic.pyuic'  # Problematic as it is executed on import
]
SKIP_MEMBERS = [
    'qApp'  # See main README.md on qApp
]

# Will contain all modules for the current binding
MODULES = []

# Flags from environment variables
QT_VERBOSE = bool(os.getenv("QT_VERBOSE"))


def read_json(filename):
    """Read JSON, return dict"""

    with open(filename, 'r') as data_file:
        return json.load(data_file)


def write_json(dictionary, filename):
    """Write dictionary to JSON"""
    with open(filename, 'w') as data_file:
        json.dump(dictionary, data_file, indent=4, sort_keys=True)
    print('--> Wrote ' + os.path.basename(filename))


def compare(dicts):
    """Compare by iteration"""

    common_members = {}
    common_keys = reduce(lambda x, y: x & y, map(dict.keys, dicts))
    for k in common_keys:
        common_members[k] = list(
            reduce(lambda x, y: x & y, [set(d[k]) for d in dicts]))

    return common_members


def copy_qtgui_to_modules():
    """Copies the QtGui list of PySide/PyQt4 into QtWidgets"""

    pyside_filepath = PREFIX + '/PySide.json'
    pyqt4_filepath = PREFIX + '/PyQt4.json'
    pyside = read_json(pyside_filepath)
    pyqt4 = read_json(pyqt4_filepath)

    # When Qt4 was moved to Qt5, they split QtGui into QtGui, QtWidgets, and
    # QtPrintSupport.
    pyside['QtWidgets'] = pyside['QtGui']
    pyqt4['QtWidgets'] = pyqt4['QtGui']
    pyside['QtPrintSupport'] = pyside['QtGui']
    pyqt4['QtPrintSupport'] = pyqt4['QtGui']

    write_json(pyside, pyside_filepath)
    print('--> Copied QtGui to QtWidgets and QtPrintSupport for {0}'.format(
        os.path.basename(pyside_filepath)))
    write_json(pyqt4, pyqt4_filepath)
    print('--> Copied QtGui to QtWidgets and QtPrintSupport for {0}'.format(
        os.path.basename(pyqt4_filepath)))


def sort_common_members():
    """Sorts the keys and members"""

    filename = PREFIX + '/common_members.json'
    sorted_json_data = {}
    json_data = read_json(filename)

    all_keys = []
    for key, value in json_data.items():
        all_keys.append(key)
    sorted_keys = sorted(all_keys)

    for key in sorted_keys:
        if len(json_data[key]) > 0:
            # Only add modules which have common members
            sorted_json_data[key] = sorted(json_data[key])

    print('--> Sorted/cleaned ' + os.path.basename(filename))

    write_json(sorted_json_data, filename)


def generate_common_members():
    """Generate JSON with commonly shared members"""

    pyside = read_json(PREFIX + '/PySide.json')
    pyside2 = read_json(PREFIX + '/PySide2.json')
    pyqt4 = read_json(PREFIX + '/PyQt4.json')
    pyqt5 = read_json(PREFIX + '/PyQt5.json')

    dicts = [pyside, pyside2, pyqt4, pyqt5]
    common_members = compare(dicts)
    write_json(common_members, PREFIX + '/common_members.json')


if __name__ == '__main__':
    # Parse commandline arguments
    parser = OptionParser()
    parser.add_option('--binding', dest='binding', metavar='BINDING')
    parser.add_option(
        '--copy-qtgui',
        action='store_true',
        dest='copy',
        default=False)
    parser.add_option(
        '--generate-common-members',
        action='store_true',
        dest='generate',
        default=False)
    parser.add_option(
        '--sort-common-members',
        action='store_true',
        dest='sort',
        default=False)
    (options, args) = parser.parse_args()

    if options.copy:
        copy_qtgui_to_modules()

    elif options.generate:
        generate_common_members()

    elif options.sort:
        sort_common_members()

    else:

        # Import <binding>
        binding = __import__(options.binding)

        for importer, modname, ispkg in pkgutil.walk_packages(
                path=binding.__path__,
                prefix=binding.__name__ + '.',
                onerror=lambda x: None):
            if modname not in SKIP_MODULES:
                MODULES.append(modname)
                basemodule = modname[:modname.rfind('.')]
                submodule = modname[modname.rfind('.')+1:]
                try:
                    import_statement = (
                        'from ' + basemodule + ' import ' + submodule)
                    exec(import_statement)
                    # print(import_statement)
                except (ImportError, AttributeError, SyntaxError) as error:
                    # SyntaxError catched here because e.g. _port3
                    # running on Python 2...
                    print('WARNING: Skipped import', modname, error)

                try:
                    raw_members = []  # avoid Hound errors
                    exec('raw_members = dir(' + submodule + ')')
                    members = []
                    for member in raw_members:
                        if member not in SKIP_MEMBERS and \
                                not member.startswith('_'):
                            try:
                                import_statement = (
                                    'from ' + basemodule + '.' + submodule +
                                    ' import ' + member)
                                exec(import_statement)
                                # print(import_statement)
                                MODULES.append(modname + '.' + member)
                            except (AttributeError, SyntaxError) as error:
                                # SyntaxError catched here because e.g. _port3
                                # running on Python 2...
                                print('WARNING: Skipped import',
                                      modname, error)
                except (NameError) as error:
                    print('WARNING: Skipped dir() command', modname, error)

        # Remove duplicates and sort
        MODULES = sorted(list(set(MODULES)))

        if QT_VERBOSE:
            # Print all modules (for debugging)
            for module in MODULES:
                print(module)

        # Create dictionary
        members = {}
        for module in MODULES:
            key = module.split('.')[1]
            if key not in members:
                members[key] = []
            try:
                value = module.split('.')[2]
                members[key].append(value)
            except IndexError:
                pass

        # Sort and remove duplicates
        sorted_members = {}
        for key, value in members.copy().items():
            sorted_members[key] = sorted(list(set(value)))

        if QT_VERBOSE:
            # Debug
            pprint(sorted_members)

        # Write to disk
        filepath = PREFIX + '/' + binding.__name__ + '.json'
        write_json(sorted_members, filepath)
