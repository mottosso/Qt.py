FROM ubuntu:14.04
RUN apt-get update && apt-get install -y \
    python-qt4 \
    python-pyside \
    python3-pyqt4 \
    python3-pyside \
    python-pip
RUN pip install supervisor nose
RUN mkdir -p /var/log/supervisor