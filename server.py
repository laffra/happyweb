#!python
import urlparse
import urllib2
import httplib
from SocketServer import ThreadingMixIn
from  BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import time
import sites
import json
import re

class ThreadingServer(ThreadingMixIn, HTTPServer):
    pass

PORT_NUMBER = 9137

class RequestHandler(SimpleHTTPRequestHandler):

  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type','text/html')
    self.end_headers()
    args = urlparse.parse_qs(urlparse.urlparse(self.path).query)
    if "url" in args:
      domain = args['url'][0]
      url = "http://" + domain
      start = time.time()
      try:
        html = urllib2.urlopen(url, timeout=10).read()
      except Exception as e:
        if "CERTIFICATE" not in str(e) and "Forbidden" not in str(e):
          return
      end = time.time()
      if end - start > 10.0:
        return
      message = "%.2f" % (end - start)
      print("Loaded " + url + " " + message)
      self.wfile.write(message)
    elif self.path.endswith("sites"):
      self.wfile.write(json.dumps(sites.sites))
    else:
      with open("index.html") as fin:
        self.wfile.write(fin.read())
    return

try:
  server = ThreadingServer(('', PORT_NUMBER), RequestHandler)
  server.serve_forever()
except KeyboardInterrupt:
	server.socket.close()