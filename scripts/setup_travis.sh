#!/bin/bash

set -ev

mkdir bin
export PATH="$PATH:`pwd`/bin"

echo "DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
echo "${DRIVER}"

if [ "${DRIVER}" = "phantomjs" ]; then
  echo "using phantomjs"
  wget -O - https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 | tar -xj
  mv phantomjs-2.1.1-linux-x86_64/bin/phantomjs bin
  phantomjs --version
fi

if [ "${DRIVER}" = "firefox" ]; then
  echo "using firefox"
  wget -O - https://github.com/mozilla/geckodriver/releases/download/v0.10.0/geckodriver-v0.10.0-linux64.tar.gz | tar xvzf -
  mv geckodriver bin
  geckodriver --version
fi

if [ "${DRIVER}" = "chrome" ]; then
  sleep 1
fi
