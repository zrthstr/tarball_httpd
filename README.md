# tarHTTPd
* tarHTTPd extends pythons http.server to serve directroys as tarballs without creating the tarball in memory.
* as much code as possible has been taken from python3's `org/http/server.py`

### Usage
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


# todo:
* fix .. button
* add option to tar '.' and name correctly
* check if archive is created in memory or streamed
* add zip, non compressed zip, and gz support
* make sure memory is not wasted
* fix symlink hack
* fix dir listing name in html page
* add port, bind and dir paramters
* test, test, test
* make pip package

