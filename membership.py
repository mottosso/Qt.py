import os
import pkgutil
import json
from optparse import OptionParser
from functools import reduce

# This is where all files are read from and saved to
PREFIX = '/Qt.py'

# These are not only imported but also executed
SKIP = ['PyQt4.uic.pyuic', 'PyQt5.uic.pyuic']

# Will contain all modules for the current binding
MODULES = []


def read_json(filename):
    """Read JSON, return dict"""

    with open(filename, 'r') as data_file:
        return json.load(data_file)


def write_json(dictionary, filename):
    """Write dictionary to JSON"""
    with open(filename, 'w') as data_file:
        json.dump(dictionary, data_file, indent=4)
    print('--> Wrote ' + os.path.basename(filename))


def compare(dicts):
    """Compare by iteration"""

    common_members = {}
    common_keys = reduce(lambda x, y: x & y, map(dict.keys, dicts))
    for k in common_keys:
        common_members[k] = list(
            reduce(lambda x, y: x & y, [set(d[k]) for d in dicts]))

    return common_members


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
        '--generate-common-members',
        action='store_true',
        dest='generate',
        default=False)
    (options, args) = parser.parse_args()

    if options.generate:
        generate_common_members()

    else:

        # Import <binding>
        binding = __import__(options.binding)

        for importer, modname, ispkg in pkgutil.walk_packages(
                path=binding.__path__,
                prefix=binding.__name__ + '.',
                onerror=lambda x: None):
            if modname not in SKIP:
                MODULES.append(modname)
                basemodule = modname[:modname.rfind('.')]
                submodule = modname[modname.rfind('.')+1:]
                try:
                    import_statement = (
                        'from ' + basemodule + ' import ' + submodule)
                    # print(import_statement)
                    exec(import_statement)
                except (ImportError, AttributeError, SyntaxError) as error:
                    print('IMPORT SKIP', modname, error)

                try:
                    raw_members = []  # avoid Hound errors
                    exec('raw_members = dir(' + submodule + ')')
                    members = []
                    for member in raw_members:
                        if not member.startswith('_'):
                            MODULES.append(modname + '.' + member)
                except (NameError) as error:
                    print('DIR SKIP', modname, error)

        # Remove duplicates and sort
        MODULES = sorted(list(set(MODULES)))

        # Print all modules (for debugging)
        # for module in MODULES:
        #     print(module)

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

        # Debug
        # pprint(sorted_output)

        # Write to disk
        filepath = PREFIX + '/' + binding.__name__ + '.json'
        write_json(sorted_members, filepath)
