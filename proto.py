#!/usr/bin/env python3

from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
from io import BytesIO
from urllib.parse import urlparse


class TarHTTP(SimpleHTTPRequestHandler):

    #def __init__(self, *args, directory=None, **kwargs):
    #    for l in TarHTTP.__mro__:
    #        print(l)

    def do_GET(self):
        print("in do_GET")
        args = urlparse(self.requestline).query.split(" ")[0]

        #print(dir(self))
        #print("XXX",self.requestline)
        #f = self.send_head()
        #print("f:", f)
        #print("self.wfile:", self.wfile)

        if "dl=tar" in args:
            print("Found 'dl=tar' in args")
            # SERVER_DIR_AS_TAR()
        else:
            print("Not Found 'dl=tar' in args")
            super().do_GET()
            
            #f = self.send_head()
            #if f:
            #    try:
            #        # def copyfile(self, source, outputfile):
            #        self.copyfile(f, self.wfile)
            #    finally:
            #        f.close()

        #print("--headers--\n", self.headers, "\n--end-headdes--",sep="")

    def list_directory(self, path):
        print("AA" * 40)
        return super().list_directory(path)
        #super().list_directory(path)


httpd = HTTPServer(('localhost', 8000), TarHTTP)
httpd.serve_forever()


