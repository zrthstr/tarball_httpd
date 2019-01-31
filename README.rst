tarball_httpd
==============

Serves directories as .TARs (tarball archives) over http - to be downloaded by a web browser

-  tarball\_httpd extends pythons http.server/SimpleHTTPServer to serve
   directories as tarballs
-  the goal is to do this without creating the tarball in memory at one
   time
-  as much code as possible has been borrowed from python3's http.server

Todo
----

-  doublecheck for XSS, LFI, directory traversal vulnerabilities
-  add more supported archive files: zip, non compressed zip, gz/gz2, ..
-  test on bsd, mac and windows

Install
-------

::

    % pip install tarball_httpd

Usage
-----

::

    % python -m tarball_httpd
      Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
     
    % python -m tarball_httpd 12345 --bind 127.0.0.1 --directory /tmp
      Serving HTTP on 127.0.0.1 port 12345 (http://127.0.0.1:12345/) ..

    % python -m tarball_httpd -h                               
      usage: tarball_httpd.py [-h] [--bind ADDRESS] [--directory DIRECTORY] [port]

      positional arguments:
        port                  Specify alternate port [default: 8000]

      optional arguments:
        -h, --help            show this help message and exit
        --bind ADDRESS, -b ADDRESS
                            Specify alternate bind address [default: all interfaces]
        --directory DIRECTORY, -d DIRECTORY
                            Specify alternative directory [default:current directory]

Usage without installation
--------------------------

::

    % git clone git@github.com:zrthstr/tarball_httpd.git
    % cd tarball_httpd
    % ./tarball_httpd.py
      Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...

Testing
-------

::

    % ./tests/test.sh

License
-------
This project is licensed under the PSF License - see the `LICENSE <./LICENSE>`_ file for details


Authors and Acknowledgments
---------------------------
Largs parts of its code are based on or copied from python3/lib/http/server

tarball_httpd was written by zrth1k@gmail.com
