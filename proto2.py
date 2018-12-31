#!/usr/bin/env python3

from http.server import HTTPServer, SimpleHTTPRequestHandler
import re
#from urllib.parse import urlparse

import tarfile
import datetime
import email.utils
import html
import io
import os
import sys
import urllib.parse

from http import HTTPStatus

__version__ = "0.1"

class TarHTTPd(SimpleHTTPRequestHandler):

    """Simple HTTP request handler with GET and HEAD commands.

    This serves files from the current directory and any of its
    subdirectories.  The MIME type for files is determined by
    calling the .guess_type() method.

    The GET and HEAD requests are identical except that the HEAD
    request omits the actual contents of the file.

    """

    server_version = "SimpleHTTP/" + __version__

    def __init__(self, *args, directory=None, **kwargs):
        if directory is None:
            directory = os.getcwd()
        self.directory = directory
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Serve a GET request."""

        args = urllib.parse.urlparse(self.requestline).query

        if "dl=tar" in args:
            self.do_GET_TAR()
        else:
            super().do_GET()

    def do_GET_TAR(self):
        """ send 'virtual' tar file to pipe and copy to socket """

        path = self.translate_path(self.path)
        path = re.sub('\.tar$', '', path)
        parts = urllib.parse.urlsplit(self.path)
        print(parts)

        if os.path.isdir(path):
            print("is_dir:", path)
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", 'application/x-tar')
            #self.send_header("Content-Lenght", '56620')
            self.send_header("Content-Lenght", '620')
            #self.send_header("Last-Modified", 'Fri, 14 Dec 2018 07:24:02 GMT')
            self.end_headers()
            sample = '/home/zrth/test/tarHTTPd/test.tar'
            #f = open(sample,'rb')
            #print(dir(f))
            #print(type(f))
            some_file = '/home/zrth/test/tarHTTPd/README.md'

            pr, pw = os.pipe()
            ppr  = os.fdopen(pr, 'rb')
            ppw  = os.fdopen(pw, 'wb')

            with tarfile.open(name="hooks.tar", mode="w|", fileobj=ppw, encoding='utf-8') as out:
                out.add(some_file)

            os.close(pw)
            self.copyfile(ppr, self.wfile)
            os.close(pr)

        else:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found (tar)")
            return None
        
#    def do_HEAD(self):
#        """Serve a HEAD request."""
#        f = self.send_head()
#        if f:
#            f.close()
#
    def send_head(self ):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            parts = urllib.parse.urlsplit(self.path)
            if not parts.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(HTTPStatus.MOVED_PERMANENTLY)
                new_parts = (parts[0], parts[1], parts[2] + '/',
                             parts[3], parts[4])
                new_url = urllib.parse.urlunsplit(new_parts)
                self.send_header("Location", new_url)
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None

        try:
            fs = os.fstat(f.fileno())
            # Use browser cache if possible
            if ("If-Modified-Since" in self.headers
                    and "If-None-Match" not in self.headers):
                # compare If-Modified-Since and time of last file modification
                try:
                    ims = email.utils.parsedate_to_datetime(
                        self.headers["If-Modified-Since"])
                except (TypeError, IndexError, OverflowError, ValueError):
                    # ignore ill-formed values
                    pass
                else:
                    if ims.tzinfo is None:
                        # obsolete format with no timezone, cf.
                        # https://tools.ietf.org/html/rfc7231#section-7.1.1.1
                        ims = ims.replace(tzinfo=datetime.timezone.utc)
                    if ims.tzinfo is datetime.timezone.utc:
                        # compare to UTC datetime of last modification
                        last_modif = datetime.datetime.fromtimestamp(
                            fs.st_mtime, datetime.timezone.utc)
                        # remove microseconds, like in If-Modified-Since
                        last_modif = last_modif.replace(microsecond=0)

                        if last_modif <= ims:
                            self.send_response(HTTPStatus.NOT_MODIFIED)
                            self.end_headers()
                            f.close()
                            return None

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", ctype)
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified",
                self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise

    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(
                HTTPStatus.NOT_FOUND,
                "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        r = []
        try:
            displaypath = urllib.parse.unquote(self.path,
                                               errors='surrogatepass')
        except UnicodeDecodeError:
            displaypath = urllib.parse.unquote(path)
        displaypath = html.escape(displaypath, quote=False)
        enc = sys.getfilesystemencoding()
        title = 'Directory listing for %s' % displaypath
        r.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                 '"http://www.w3.org/TR/html4/strict.dtd">')
        r.append('<html>\n<head>')
        r.append('<meta http-equiv="Content-Type" '
                 'content="text/html; charset=%s">' % enc)
        r.append('<title>%s</title>\n</head>' % title)
        r.append('<body>\n<h1>%s</h1>' % title)
        r.append('<hr>\n<ul>')

        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
                tarname = name + ".tar"
                tarname_secure = urllib.parse.quote(tarname, errors='surrogatepass') + "?dl=tar" 

                r.append('<li><a href="%s">%s</a>   <a href="%s">(tar)</a>  </li>' % (urllib.parse.quote(linkname, errors='surrogatepass'), html.escape(displayname, quote=False), tarname_secure))

#### TODO: figure out what to do with symlinks to files, and symlinks to dirs
#            if os.path.islink(fullname):
#                displayname = name + "@"
#                # Note: a link to a directory displays with @ and links with /
            else:
                r.append('<li><a href="%s">%s</a></li>' % (urllib.parse.quote(linkname, errors='surrogatepass'), html.escape(displayname, quote=False)))

        r.append('</ul>\n<hr>\n</body>\n</html>\n')
        encoded = '\n'.join(r).encode(enc, 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f



if __name__ == "__main__":
    httpd = HTTPServer(('localhost', 8000), TarHTTPd)
    httpd.serve_forever()

