FROM ubuntu:14.04

RUN apt-get update && apt-get install -y \
    python-qt4 \
    python-pyside \
    python-pip

# Nose is the Python test-runner
RUN pip install nose nosepipe

# Enable additional output from Qt.py
ENV QT_VERBOSE true

ENTRYPOINT nosetests --verbose --with-process-isolation /Qt.py/tests.py
