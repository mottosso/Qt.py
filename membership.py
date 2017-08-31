import pkgutil


BINDINGS = (__import__('PySide'), __import__('PySide2'), __import__('PyQt4'),
            __import__('PyQt5'))

MODULES = []

if __name__ == '__main__':
    for package in BINDINGS:
        for importer, modname, ispkg in pkgutil.walk_packages(
                path=package.__path__,
                prefix=package.__name__ + '.',
                onerror=lambda x: None):
            MODULES.append(modname)
            base = modname[:modname.rfind('.')]
            mod = modname[modname.rfind('.')+1:]
            try:
                exec('from ' + base + ' import ' + mod)
                raw_members = []  # avoid Hound errors
                exec('raw_members = dir(' + mod + ')')

                members = []
                for member in raw_members:
                    if not member.startswith('_'):
                        print(modname + '.' + member)
                        MODULES.append(modname + '.' + member)
            except:
                pass

    for modname in MODULES:
        print(modname)
