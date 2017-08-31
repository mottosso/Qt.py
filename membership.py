import pkgutil


BINDINGS = (__import__('PySide'), __import__('PySide2'), __import__('PyQt4'),
            __import__('PyQt5'))


if __name__ == '__main__':
    for package in BINDINGS:
        for importer, modname, ispkg in pkgutil.walk_packages(
                path=package.__path__,
                prefix=package.__name__ + '.',
                onerror=lambda x: None):
            print(modname)
