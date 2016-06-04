FROM ubuntu:14.04
RUN apt-get update && apt-get install -y \
    python-qt4 \
    python-pyside \
    python-pip
RUN pip install nose
ENTRYPOINT nosetests --verbose /Qt.py/tests.py