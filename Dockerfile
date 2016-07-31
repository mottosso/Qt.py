FROM ubuntu:14.04

RUN apt-get update && apt-get install -y \
    python-qt4 \
    python-pyside \
    python-pip \
    xvfb

# Nose is the Python test-runner
RUN pip install nose nosepipe xvfbwrapper

# Enable additional output from Qt.py
ENV QT_VERBOSE true

WORKDIR /workspace/Qt.py
ENTRYPOINT cp -r /Qt.py /workspace && \
	python build_caveats_tests.py && \
	nosetests \
		--verbose \
		--with-process-isolation \
		--with-doctest \
		--exe
