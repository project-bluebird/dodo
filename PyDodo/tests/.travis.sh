#!/bin/bash
set -ev
cd $DODO_HOME/PyDodo/ && pytest -vs tests/
# Test docker on Linux only as docker not yet supported on macOS within travis
if [ $TRAVIS_OS_NAME = "linux" ]; then
    docker-compose up -d
    sleep 20
    docker-compose down
fi
# Run full integration tests
if [ $TRAVIS_OS_NAME = linux ]; then
    docker-compose up -d
    sleep 20
    cd $DODO_HOME/PyDodo/
    pytest -vs tests/
    docker-compose down
fi
