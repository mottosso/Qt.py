from optparse import OptionParser
import pkgutil
import json

# These are not only imported but also executed
SKIP = ['PyQt4.uic.pyuic', 'PyQt5.uic.pyuic']

# Will contain all modules for the current binding
MODULES = []

# Parse commandline argument "--binding"
parser = OptionParser()
parser.add_option(
    "-b",
    "--binding",
    dest="binding",
    metavar="BINDING")
(options, args) = parser.parse_args()

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
            import_statement = 'from ' + basemodule + ' import ' + submodule
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
with open('/Qt.py/' + binding.__name__ + '.json', 'w') as f:
    json.dump(sorted_members, f, indent=4)
