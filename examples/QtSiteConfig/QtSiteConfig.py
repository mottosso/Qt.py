# Contrived example used for unit testing. For a more realistic example
# see the README

def update_members(members, step):
    """This function is called by Qt.py to modify the modules it exposes.

    Arguments:
        members (dict): The members considered by Qt.py
        step (str): Used to identify what members will be used for.
    """

    if step == 'common':
        # Contrived example used for unit testing. This makes the QtCore module
        # not accessible. I chose this so it can be tested everywhere, for a
        # more realistic example see the README
        members.pop("QtCore")

    elif step == 'compatibility':
        # Create a QtCompat.QWidget compatibility class. This example is
        # is used to provide a testable unittest
        for binding in ("PySide2", "PyQt5", "PySide", "PyQt4"):
            members[binding]["QWidget"] = {
                # Simple remapping of QWidget.windowTitle
                "windowTitleTest": "_QtWidgets.QWidget.windowTitle",
                # Remap QWidget.windowTitle with a decorator that modifies
                # the returned value.
                "windowTitleDecorator": "_QtWidgets.QWidget.windowTitle",
            }

def update_compatibility_decorators(binding, decorators):
    """ This function is called by Qt.py to modify the decorators applied to
    QtCompat namespace objects. Defining this method is optional.

    Arguments:
        binding (str): The Qt binding being wrapped by Qt.py
        decorators (dict): Maps specific decorator functions to
            QtCompat namespace functions. See Qt._build_compatibility_members
            for more info.
    """

    def _testFunction(some_function):
        def wrapper(*args, **kwargs):
            ret = some_function(*args, **kwargs)
            # Modifies the returned value so we can test that the
            # decorator works.
            return 'Test: {}'.format(ret)
        # preserve docstring and name of original function
        wrapper.__doc__ = some_function.__doc__
        wrapper.__name__ = some_function.__name__
        return wrapper

    # Install the decorator so it will be applied to the QtCompat object
    decorators['windowTitleDecorator:_QtWidgets.QWidget.windowTitle'] = \
        _testFunction
