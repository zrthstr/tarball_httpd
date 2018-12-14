#!/usr/bin/env python3

from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
from io import BytesIO
from urllib.parse import urlparse


class TarHTTP(SimpleHTTPRequestHandler):

    def do_GET(self):
        print("in do_GET")
        print(dir(self))
        print("XXX",self.requestline)
        args = urlparse(self.requestline).query.split(" ")[0]
        if "dl=tar" in args:
            print("Found 'dl=tar' in args")
            ffff = open("/tmp/out")
            self.copyfile(ffff, self.wfile)
        else:
            print("nope")
            self.really_do_GET()

        print(self.headers)


    def really_do_GET(self):
        print("in really_do_GET")
        f = self.send_head()
        if f:
            try:
                # def copyfile(self, source, outputfile):
                self.copyfile(f, self.wfile)
            finally:
                f.close()


httpd = HTTPServer(('localhost', 8000), TarHTTP)
httpd.serve_forever()


