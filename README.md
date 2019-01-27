# tarball_httpd
Server directories as tarball archive for download over http

* tarball_httpd extends pythons http.server to serve directroys as tarballs.
* the goal is to do this without creating the tarball in memory.
* as much code as possible has been taken from python3's `org/http/server.py`

## Todo:
* make tar paths rellative
* add screenshot to readme
* make paramertes cant be manipulated to do funny things
* doublecheck XSS and so on are possible
* add option to tar '.' and name correctly
* check if archive is created in memory or streamed
* add more supported archive files: zip, non compressed zip, gz/gz2
* fix symlink hack
* fix dir listing name in html page
* test, test, test
* move from demo.pypi to prod
* add banner

## git clone and use
```
git clone https://github.com/zrthstr/tarball_httpd
cd tarball_httpd
./tarball_httpd.py -d /tmp
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ..
```

## install
`% pip install tarball_httpd`

## usage
```
% python -m tarball_httpd
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

```
% python -m tarball_httpd 12345 --bind 127.0.0.1 --directory /tmp
Serving HTTP on 127.0.0.1 port 12345 (http://127.0.0.1:12345/) ..
```

```
% python -m tarball_httpd 12345 -h                               
usage: __main__.py [-h] [--bind ADDRESS] [--directory DIRECTORY] [port]

positional arguments:
  port                  Specify alternate port [default: 8000]

optional arguments:
  -h, --help            show this help message and exit
  --bind ADDRESS, -b ADDRESS
                        Specify alternate bind address [default: all
                        interfaces]
  --directory DIRECTORY, -d DIRECTORY
                        Specify alternative directory [default:current
                        directory
```

## testing
```
./tests/test.sh 
```

## debugging
```
curl 'http://localhost:12345/testin/testdir.tar?dl=tar' -vvvv --output - 

sudo tcpdump -nnSX -i lo port 12345 -XX

alias cu='curl "http://localhost:12345/testin/testdir.tar?dl=tar" -vvvv --output -'
for 1 in range $(seq 1 100); do cu ; sleep 1 ; done
```
