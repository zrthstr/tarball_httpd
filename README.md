# tarball_httpd
Serves directories as .TARs (tarball archive) over http - for them to be downloaded by a web browser

* tarball_httpd extends pythons http.server/SimpleHTTPServer to serve directroies as tarballs
* the goal is to do this without creating the tarball in memory
* as much code as possible has been borrowed from python3's http.server

## Todo
* make tar paths rellative
* add screenshot for readme 
* add github page
* make paramertes cant be manipulated to do funny things
* doublecheck XSS and so on are possible
* check if archive is created in memory or streamed
* add more supported archive files: zip, non compressed zip, gz/gz2
* move from demo.pypi to prod
* test other platforms than linux

## Install
    % pip install tarball_httpd

## Usage
    % python -m tarball_httpd
    Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
    
    % python -m tarball_httpd 12345 --bind 127.0.0.1 --directory /tmp
    Serving HTTP on 127.0.0.1 port 12345 (http://127.0.0.1:12345/) ..


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

## Usage without installation and testing
    % git clone git@github.com:zrthstr/tarball_httpd.git
    % cd tarball_httpd.py


    % ./tarball_httpd.py
        Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...


    % ./tests/test.sh
        ....


