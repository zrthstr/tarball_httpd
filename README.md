# TarHTTPServer

* TarHTTPServer extends pythons http.server to serve directroys as tarballs.
* the goal is to do this without creating the tarball in memory.
* as much code as possible has been taken from python3's `org/http/server.py`

### Todo:
* make this a python module
* integrate in https://test.pypi.org/
* more fixing
* integrate in https://pypi.org/
* add option to tar '.' and name correctly
* check if archive is created in memory or streamed
* add more supported archive files: zip, non compressed zip, gz/gz2
* fix symlink hack
* fix dir listing name in html page
* add dir paramters
* test, test, test
* make pip package

# future
### install
`% pip install TarHTTPServer`

### usage
`% python -m TarHTTPServer`

```
# set port
% python -m TarHTTPServer 8080
```

```
# set bind addr and port
% python -m TarHTTPServer --bind 127.0.0.1 8080
```


# OLD
### Usage
```
% ./tarHTTPserver.py
```

```
% ./tarHTTPserver.py -h
usage: tarHTTPserver.py [-h] [--bind ADDRESS] [port]

positional arguments:
  port                  Specify alternate port [default: 8000]

optional arguments:
  -h, --help            show this help message and exit
  --bind ADDRESS, -b ADDRESS
                        Specify alternate bind address [default: all
                        interfaces]
```

```
% ./tarHTTPserver.py --bind 127.0.0.1 8080
```


