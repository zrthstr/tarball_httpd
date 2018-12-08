from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler

from io import BytesIO

from urllib.parse import urlparse


dir(SimpleHTTPRequestHandler)

class TarHTTP(SimpleHTTPRequestHandler):

	def foo(self):
		print("DDDD")

	def do_GET(self):
		print("FFFFF")
		print(dir(self))
		print("XXX",self.requestline)
		args = urlparse(self.requestline).query.split(" ")[0]
		if "dl=tar" in args:
			print("!!!!!!!")
			ffff = open("/tmp/out")
			self.copyfile(ffff, self.wfile)
		else:
			print("nope")
			self.really_do_GET()


	def really_do_GET(self):
		print("TTTTTTT")
		f = self.send_head()
		if f:
			try:
				# def copyfile(self, source, outputfile):
				self.copyfile(f, self.wfile)
			finally:
				f.close()


httpd = HTTPServer(('localhost', 8000), TarHTTP)
httpd.serve_forever()


