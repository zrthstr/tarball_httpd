#!/usr/bin/env python

""" Tar HTTP server class.

SECURITY WARNING: DON'T USE THIS CODE UNLESS YOU ARE INSIDE A FIREWALL
-- it has not been thoroughly checked for seurity vulnerabilitys.

Note: See /usr/lib/python3.7/http/server.py
http.server is the origin to much of this code.


XXX To do:
- add tests
- more testing
- more logging
- check for xxs, unexpected symlink behaviour
- make sure big tar files are not built in memory but streamed
- add support for zip, noncmpressed zip, and tar.gz

"""


import re
import tarfile
import argparse
import threading
import html
import io
import os
import sys
import urllib.parse
from functools import partial

from http.server import SimpleHTTPRequestHandler, test
from http import HTTPStatus

__version__ = '0.0.2'


class TarHTTPServer(SimpleHTTPRequestHandler):
    """Tar HTTP request handler with GET and HEAD commands.

    This serves dircetorys as tars and files from the current directory and any of its
    subdirectories.  The MIME type for files is determined by
    calling the .guess_type() method.

    The GET and HEAD requests are identical except that the HEAD
    request omits the actual contents of the file.

    """

    server_version = "tarball_HTTPd/" + __version__


    def do_GET(self):
        """Serve a GET request."""

        args = urllib.parse.urlparse(self.requestline).query
        if "dl=tar" in args:
            self.do_TAR()
        else:
            super().do_GET()


    def tar_pipe_feed(self, name, pipe, directory):
        """ Tar Thread.

        Adds all files from directory to tarobj.
        Writes tarobj to pipe.
        Closes pipe when read is done and exists thread.
        """
        with tarfile.open(name=name, mode="w|", fileobj=pipe,
                          encoding='utf-8', bufsize=20 * 512) as tar:
            tar.add(directory, arcname=os.path.basename(os.path.normpath(directory)))
        pipe.close()


    def do_TAR(self):
        """ Takes care of HTTP things related to serving a tar

        Sends correct Content-type.
        Starts tar_pipe_feed thread.
        Takes care of file copying.
        """

        self.full_tar_name = self.translate_path(self.path)
        self.out_tar_name = os.path.split(self.full_tar_name)[-1]
        self.full_chosen_dir = re.sub(r'\.tar$', '', self.full_tar_name)

        if os.path.isdir(self.full_chosen_dir):
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", 'application/x-tar')
            self.end_headers()
            fh_r, fh_w = os.pipe()
            pipe_r = os.fdopen(fh_r, 'rb')
            pipe_w = os.fdopen(fh_w, 'wb')
            threading.Thread(target=self.tar_pipe_feed,
                             args=(self.out_tar_name, pipe_w, self.full_chosen_dir),
                             daemon=True).start()
            self.copyfile(pipe_r, self.wfile)
            os.close(fh_r)
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found (tar)")


    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            dlist = os.listdir(path)
        except OSError:
            self.send_error(
                HTTPStatus.NOT_FOUND,
                "No permission to list directory")
            return None
        dlist.sort(key=lambda a: a.lower())
        r = []
        try:
            displaypath = urllib.parse.unquote(self.path,
                                               errors='surrogatepass')
        except UnicodeDecodeError:
            displaypath = urllib.parse.unquote(path)
        displaypath = html.escape(displaypath, quote=False)
        enc = sys.getfilesystemencoding()
        #title = 'Directory listing for %s <a href=> (tar)' % displaypath

        cwd_path = '../' + displaypath.replace('/', '') + '.tar'

        title = ('Directory listing for %s <a href=%s?dl=tar>'
                 '<h6 style="display:inline">(tar)</h6></a>') % (displaypath, cwd_path)
        li_line = ('<li><a href="%s">%s</a> <a href="%s">'
                   '<h5 style="display:inline">(tar)</h5></a></li>')
        r.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                 '"http://www.w3.org/TR/html4/strict.dtd">')
        r.append('<html>\n<head>')
        r.append('<meta http-equiv="Content-Type" '
                 'content="text/html; charset=%s">' % enc)
        r.append('<title>%s</title>\n</head>' % title)
        r.append('<body>\n<h1>%s</h1>' % title)
        r.append('<hr>\n<ul>')

        for displayname in dlist:
            fullname = os.path.join(path, displayname)
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                tarname = displayname + ".tar"
                tarname_secure = urllib.parse.quote(tarname, errors='surrogatepass') + "?dl=tar"
                r.append(li_line % (urllib.parse.quote(displayname, errors='surrogatepass'),
                                    html.escape(displayname, quote=False), tarname_secure))

            #if os.path.islink(fullname):
            #    displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /

            else:
                r.append('<li><a href="%s">%s</a></li>' %
                         (urllib.parse.quote(displayname, errors='surrogatepass'),
                          html.escape(displayname, quote=False)))

        banner = '<p><em><font color=#484848>{}</font></a></em></p>'.format(self.server_version)
        r.append('</ul>\n<hr>\n{}\n</body>\n</html>\n'.format(banner))
        encoded = '\n'.join(r).encode(enc, 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f


def main():
    """ Parse args and call TarHTTPServer."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--bind', '-b', default='', metavar='ADDRESS',
                        help='Specify alternate bind address [default: all interfaces]')
    parser.add_argument('--directory', '-d', default=os.getcwd(),
                        help='Specify alternative directory [default:current directory]')
    parser.add_argument('port', action='store',
                        default=8000, type=int, nargs='?',
                        help='Specify alternate port [default: 8000]')
    args = parser.parse_args()

    handler_class = partial(TarHTTPServer, directory=args.directory)
    test(HandlerClass=handler_class, port=args.port, bind=args.bind)


if __name__ == "__main__":
    main()
