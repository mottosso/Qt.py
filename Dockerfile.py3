FROM ubuntu:14.04

RUN apt-get update && apt-get install -y \
    python3-pyqt4 \
    python3-pyside \
    python3-pip

# Nose is the Python test-runner
RUN pip3 install nose

# Enable additional output from Qt.py
ENV QT_VERBOSE true

ENTRYPOINT nosetests --verbose /Qt.py/tests.py