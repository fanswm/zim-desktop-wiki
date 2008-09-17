
import BaseHTTPServer

from zim.formats import wiki, html
from zim.formats.base import ParserError

class HTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	def do_GET(self):
		path = '/home/pardus/code/zim.debug/Home.txt'
		
		try:
			tree = wiki.Parser().parse_file(path)
		except ParserError, error:
			self.send_error(500, 'BUG in parser:\n'+str(error))
			return
		
		try:
			content = html.Dumper().dump_string(tree)
		except ParserError, error:
			self.send_error(500, 'BUG in dumper:\n'+str(error))
			return

		self.send_response(200) # OK
		self.send_header('Content-Type', 'text/html')
		self.send_header('Content-Length', str(len(content)))
		# Last-Modified
		# etc.
		self.end_headers()
		
		for line in content.splitlines():
			self.wfile.write(line)



	#def do_HEAD(self)