#!/bin/bash

set -ev

mkdir bin
export PATH="$PATH:`pwd`/bin"

if [ "${DRIVER}" = "phantomjs" ]; then
  wget -O - https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 | tar -xj
  mv phantomjs-2.1.1-linux-x86_64/bin/phantomjs bin
fi

if [ "${DRIVER}" = "firefox" ]; then
  wget -O - https://github.com/mozilla/geckodriver/releases/download/v0.10.0/geckodriver-v0.10.0-linux64.tar.gz | tar xvzf -
  mv geckodriver bin
fi

if [ "${DRIVER}" = "chrome" ]; then
  sleep 1
fi
