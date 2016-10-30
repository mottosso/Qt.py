## Contributing to Qt

Thanks for taking the time to contribute!

In here you'll find a series of guidelines for how you can make Qt.py better suit your needs and the needs of the target audience - film, games and tv.

Qt.py was born to address the growing needs in these industries for the development of software capable of running with more than a single flavor of the Qt bindings for Python - PySide, PySide2, PyQt4 and PyQt5.

**Table of contents**

- [Development goals](#development-goals)
  - [Support co-existence](#support-co-existence)
  - [Keep it simple](#keep-it-simple)
  - [No wrappers](#no-wrappers)
- [How can I contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Pull Requests](#pull-requests)
- [Style](#style)
  - [Commits](#commits)
  - [Version bumping](#version-bumping)
  - [Making a release](#making-a-release)

<br>

### Development Goals

Qt.py was born in the film and visual effects industry to address the growing needs for the development of software capable of running with more than one flavor of the Qt bindings for Python - PySide, PySide2, PyQt4 and PyQt5.

| Goal                       | Description
|:---------------------------|:---------------
| [*Support co-existence*](#support-coexistence) | Qt.py should not affect other bindings running in same interpreter session.
| [*Keep it simple*](#keep-it-simple)       | One file, copy/paste installation, PEP08.
| [*No wrappers*](#no-wrappers)          | Don't attempt to fill in for missing functionality in a binding.

Each of these deserve some explanation and rationale.

<br>

##### Support co-existence

Importing or otherwise using Qt.py *cannot* break other bindings. The reason being that our user-base frequently runs multiple applications, some of them using the original binding, in the same interpreter session.

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
QtCompat.translate = translate
```

<br>

##### Keep it simple

At the end of the day, Qt.py is a middle-man. It delegates requests you make to the appropriate receiver, such as PySide2. Try and keep it that way without the added overhead of complexity.

<br>

#### No wrappers

One approach at bridging two different implementations is by implementing missing functionality yourself.

A [common example](https://gist.github.com/cpbotha/1b42a20c8f3eb9bb7cb8) of this is the differing argument signature in `loadUi` from PyQt4 versus PySide.

One problem with this approach is that bindings are already wrapping an original implementation and carries a large surface area for bugs with it. By wrapping it once more, we multiply this surface area, resulting in potential for even more obscure bugs that may take years to experience and filter out.

By instead limiting the argument signature to ones they both share, we both (1) reduce the surface area (2) avoid introducing additional bugs.

We believe neither approach is right or wrong - this is simply the approach taken here that turns out to be the easier and more robust rule to follow consistently as a team.

<br>

##### No bugs

This may seem like an impossible requirement, but hear me out. Bugs stem from implementations. Therefore, if there are no implementations, there can be no bugs.

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

Contribution comes in many flavors, some of which is simply notifying us of problems or successes, so we know what to change and not to change.

### Reporting bugs

Bug reports must include:

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

Code contributions are made by (1) forking this project and (2) making a modification to it. Ideally we would prefer it preceded by an issue where we discuss the feature or problem on a conceptual level before attempting an implementation of it.

This is where we perform code review - where we take a moment to look through and discuss potential design decisions made towards the goal you aim.

Your code will be reviewed and merged once it:

1. Does something useful
1. Provides a use case and example
1. Includes tests to exercise the change
1. Is up to par with surrounding code

The parent project ever only contains a single branch, a branch containing the latest working version of the project.

We understand and recognise that "forking" and "pull-requests" can be a daunting aspect for a beginner, so don't hesitate to ask. A pull-request should normally follow an issue where you elaborate on your desires; this is also a good place to ask about these things.

<br>

## Style

Here's how we expect your code to look and feel like.

### Commits

Commits should be well contained, as small as possible (but no smaller) and its messages should be in present-tense, imperative-style.

E.g.

```bash
# No
Changed this and did that

# No
Changes this and does that

# Yes
Change this and do that
```

The reason is that, each commit is like an action. An event. And it is perfectly possible to "cherry-pick" a commit onto any given branch. In this style, it makes more sense what exactly the commit will do to your code.

- Cherry pick "Add this and remove that"
- Cherry pick "Remove X and replace with Y"

### Version bumping

This project uses [semantic versioning](http://semver.org/) and is updated *after* a new release has been made.

For example, if the project had 100 commits at the time of the latest release and has 103 commits now, then it's time to increment. If however you modify the project and it has not yet been released, then your changes are included in the overall next release.

The goal is to make a new release per increment.

### Making a Release

Once the project has gained features, had bugs sorted out and is in a relatively stable state, it's time to make a new release.

- https://github.com/mottosso/Qt.py/releases

Each release should come with:

- An short summary of what has changed.
- A full changelog, including links to resolved issues.
 
The release is then automatically uploaded to PyPI.

```bash
$ pip install Qt.py
```

Good luck and see you soon!
