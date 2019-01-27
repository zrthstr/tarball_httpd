#!/bin/bash

# set -e
set -uo pipefail

PORT=12345
HOST=127.0.0.1
URL=http://${HOST}:${PORT}

function start_server {
    pkill -f "python ../tarball_httpd.py ${PORT}"
    if [[ $? -eq 0 ]]; then
        echo ">>> Killed old httpserver, exiting" 
        exit
    fi  
    echo -n ">>> "
    ../tarball_httpd.py ${PORT} &
    sleep 1
    SERVER_PID=$(jobs -p)
    echo ">>> Server has PID: ${SERVER_PID}"
    return $PORT
}

function stop_server {
    echo ">>> Killing Server"
    kill $SERVER_PID
}

function cleanup {
    echo ">>> Cleaning up output dir"
    rm testout/*
}

function prepare_testdata {
    echo ">>> Preparing testdata"
    [[ -d 'testin' ]] || mkdir testin
    [[ -d 'testout' ]] || mkdir testout
    dd if=/dev/zero of=testin/testdir/1M bs=1M count=1 status=none
    dd if=/dev/zero of=testin/10M bs=1M count=10 status=none
    dd if=/dev/zero of=testin/100M bs=1M count=100 status=none
}

function fetch_and_check {
    echo ">>> Fetching index.html"
    curl $URL -o testout/index.html -sS
    echo ">>> Checking index.html"
    ls -alh testout/index.html
    file testout/index.html
    md5sum testout/index.html
    echo ">>> Fetching testout/testin.tar"
    curl "$URL/testin.tar?dl=tar" -o testout/testin.tar -sS
    echo ">>> Checking testout/testin.tar"
    ls -alh testout/testin.tar
    file testout/testin.tar
    md5sum testout/testin.tar
    tar --list --verbose --file=testout/testin.tar
}


# change WD to scripts location
cd "$(dirname "$0")"

prepare_testdata
start_server
fetch_and_check
cleanup
stop_server

