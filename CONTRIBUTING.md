## Contributing to Qt

Thanks for taking the time to contribute!

In here you'll find a series of guidelines for how you can make Qt.py better suit your needs and the needs of the target audience - film, games and tv.

Qt.py was born to address the growing needs in these industries for the development of software capable of running with more than a single flavour of the Qt bindings for Python - PySide, PySide2, PyQt4 and PyQt5.

**Table of contents**

- [Development goals](#development-goals)
  - [Support co-existence](#support-co-existence)
  - [Don't get smart](#dont-get-smart)
  - [No bugs](#no-bugs)
- [How can I contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Pull Requests](#pull-requests)

<br>

### Development Goals

Tha goal for us developers, in a nutshell, is this.

1. **Support co-existence** - Qt.py should not affect other bindings running in same interpreter session.
1. **Don't get smart** - One file, copy/paste installation, keep it simple.
1. **No bugs** - No implementations == No bugs.

Each of these deserve some explanation and rationale.

<br>

##### Support co-existance

Importing or otherwise using Qt.py *cannot* break other bindings. The reason being that our userbase frequently runs multiple applications, some of them using the original binding, in the same interpreter session.

```python
# Wrong
old_translate_fn = QtWidgets.QApplication.translate

def translate(context, key, disambiguation=None, encoding=None, n=0):
    return old_translate_fn(context, key, disambiguation, n)

# Overwrite original with an incompatible version
QtWidgets.QApplication.translate = staticmethod(translate)
```

```python
# Right
...
QtWidgets.QApplication.translate_ = staticmethod(translate)
```

<br>

##### Don't get smart

At the end of the day, Qt.py is a middle-man. It delegates request you make to the appropriate reciever, such as PySide2. There are many ways in which this delegation can go, and Python - being a capable dynamic programming language - can easily make something like this simple high-level goal into a tangled mess of automatic and optimised nest of bugs.

That is why delegation is a direct mapping between source -> target binding, with little or no code in between.

<br>

##### No bugs

This may seem like an impossible requirement, but hear me out. Bugs stem from implementations. Ergo, if there are no implementations, there can be no bugs.

Qt.py merely maps one binding to look like another. Implementations are left to the source developers.

```python
# Wrong
def QWidget(source_binding, *args, **kwargs):
    # Potential bug 1
    if kwargs["__special_option"] == 0x1336:
        kwargs["__magic"] = 0x1337

    # Potential bug 2
    return getattr(source_binding, "QWidget")(*args, *kwargs)

# Potential bug 3
QtWidgets.QWidget = lambda *args, **kwargs: QWidget(PySide, *args, **kwargs)
```

```python
# Right
QtWidgets.QWidget = QtGui.QWidget  # No bugs
```

<br>

## How can I contribute?

Contribution comes in many flavours, some of which is simply notifying us of problems or successes, so we know what to change and not to change.

### Reporting bugs.

Bugreports must include:

1. Description
2. Expected results
3. Short reproducible

### Suggesting enhancements

Feature requests must include:

1. Goal (what the feature aims to solve)
2. Motivation (why *you* think this is necessary)
3. Suggested implementation (psuedocode)

Questions may also be submitted as issues.

### Pull requests

Code contributions are made by (1) forking this project and (2) making a modification to it. Your code will be reviewed and merged once it:

1. Does something useful
1. Is up to par with surrounding code

The parent project ever only contains a single branch, a branch containing the latest working version of the project.

We understand and recognise that "forking" and "pull-requests" can be a daunting aspect for a beginner, so don't hesitate to ask. A pull-request should normally follow an issue where you elaborate on your desires; this is also a good place to ask about these things.

Good luck and see you soon!
