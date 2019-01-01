# tarball_httpd

* tarball_httpd extends pythons http.server to serve directroys as tarballs.
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
`% pip install tarball_httpd`

### usage
```
% python -m tarball_httpd
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

```
# set port
% python -m tarball_httpd 12345
Serving HTTP on 0.0.0.0 port 12345 (http://0.0.0.0:12345/) ...
```

```
# set bind addr and port
% python -m tarball_httpd --bind 127.0.0.1
Serving HTTP on 127.0.0.1 port 8000 (http://127.0.0.1:8000/) ...
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


