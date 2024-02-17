import os
from setuptools import setup

os.environ["QT_PREFERRED_BINDING"] = "None"
version = __import__("Qt").__version__


classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities"
]

DESCRIPTION=(
    "Python 2 & 3 compatibility wrapper around all Qt bindings - "
    "PySide, PySide2, PyQt4 and PyQt5."
)
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
README_PATH = os.path.join(ROOT_PATH, "README.md")

setup(
    name="Qt.py",
    version=version,
    description=DESCRIPTION,
    long_description=open(README_PATH).read(),
    long_description_content_type="text/markdown",
    author="Marcus Ottosson",
    author_email="konstruktion@gmail.com",
    url="https://github.com/mottosso/Qt",
    license="MIT",
    zip_safe=False,
    py_modules=["Qt"],
    packages=["Qt-stubs"],
    package_data={"Qt-stubs": ["*.pyi"]},
    include_package_data=True,
    install_requires=["types-PySide2"],
    classifiers=classifiers
)
