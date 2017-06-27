# Contrived example used for unit testing. This makes the QtCore module
# not accessible. I chose this so it can be tested everywhere, for a more
# realistic example see the README


def update_members(members):
    """This function is called by Qt.py to modify the modules it exposes.

    Arguments:
        members (dict): The members considered by Qt.py

    """

    members.pop("QtCore")
