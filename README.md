# tarHTTPd
tarHTTPd extends pythons http.server to serve directroys as tarballs without creating the tarball in memory.

# as much code as possible has been taken from python3's `org/http/server.py`

# todo:
fix .. button
add option to tar '.' and name correctly
check if archive is created in memory or streamed
add zip, non compressed zip, and gz support
make sure memory is not wasted
fix symlink hack
fix dir listing name in html page
add port, bind and dir paramters
test, test, test
make pip package

### who this should look
```
%  curl -v  localhost:8000/test.tar -o /dev/null  

> GET /test.tar HTTP/1.1
> Host: localhost:8000
> User-Agent: curl/7.62.0
> Accept: */*
> 


< HTTP/1.0 200 OK
< Server: SimpleHTTP/0.6 Python/3.7.1
< Date: Fri, 14 Dec 2018 11:38:45 GMT
< Content-type: application/x-tar
< Content-Length: 56620
< Last-Modified: Fri, 14 Dec 2018 07:24:02 GMT
< 

```
