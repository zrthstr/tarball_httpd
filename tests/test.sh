#!/bin/bash

# set -e
set -uo pipefail

PORT=12345
HOST=127.0.0.1
URL=http://${HOST}:${PORT}

function prepare_testdata {
    echo ">>> Preparing testdata"
    [[ -d 'testin' ]] || mkdir testin
    [[ -d 'testin/testdir' ]] || mkdir testin/testdir
    [[ -d 'testout' ]] || mkdir testout
    dd if=/dev/zero of=testin/testdir/1M bs=1M count=1 status=none || exit 1
    dd if=/dev/zero of=testin/10M bs=1M count=10 status=none || exit 1 
    dd if=/dev/zero of=testin/100M bs=1M count=100 status=none || exit 1
}

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

function fetch_and_check {
    echo ">>> Fetching index.html"
    curl $URL -o testout/index.html -sS || exit 1
    echo ">>> Checking index.html"
    ls -alh testout/index.html || exit 1
    file testout/index.html || exit 1 
    md5sum testout/index.html || exit 1
    echo ">>> Fetching testout/testin.tar"
    curl "$URL/testin.tar?dl=tar" -o testout/testin.tar -sS || exit 1
    echo ">>> Checking testout/testin.tar"
    ls -alh testout/testin.tar || exit 1
    file testout/testin.tar || exit 1
    md5sum testout/testin.tar || exit 1
    tar --list --verbose --file=testout/testin.tar || exit 1
}

function cleanup {
    echo ">>> Cleaning up output dir"
    rm testout/*
}

function stop_server {
    echo ">>> Killing Server"
    kill $SERVER_PID
}


# change WD to scripts location
cd "$(dirname "$0")"

prepare_testdata
start_server
fetch_and_check
cleanup
stop_server

