FROM ubuntu:14.04

RUN apt-get update && apt-get install -y \
    python-qt4 \
    python-pyside \
    python-pip
<<<<<<< develop

# Nose is the Python test-runner
RUN pip install nose

# Enable additional output from Qt.py
ENV QT_VERBOSE true

ENTRYPOINT nosetests --verbose /Qt.py/tests.py
=======
RUN pip install nose nosepipe
ENTRYPOINT nosetests --verbose --with-process-isolation /Qt.py/tests.py
>>>>>>> Implement nosepipe
