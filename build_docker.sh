docker build . -f Dockerfile-build-py2.7 -t fredrikaverpil/qtpytest2.7:latest > build2.7.log 2>&1
docker build -t mottosso/qt.py27 -f Dockerfile-py2.7 .
docker build . -f Dockerfile-build-py3.4 -t fredrikaverpil/qtpytest3.4:latest > build3.4.log 2>&1
docker build -t mottosso/qt.py34 -f Dockerfile-py3.4 .
