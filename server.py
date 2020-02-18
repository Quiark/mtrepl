import os
import sys
import json
import pdb

from http.server import HTTPServer, BaseHTTPRequestHandler

codestore = []

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        #pdb.set_trace()
        print(self.path)
        if self.path == '/code/add':
            self.add_code()
        elif self.path == '/code/get':
            self.get_code()
        else:
            self.wfile.write(b'nothing here')

    def do_POST(self):
        return self.do_GET()

    def add_code(self):
        global codestore
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()

        codestore.append(json.loads(body))

    def get_code(self):
        global codestore
        jsdat = json.dumps(codestore).encode()
        print(codestore)

        self.send_response(200)
        self.send_header('content-type', 'application/json')
        self.send_header('content-length', len(jsdat))
        self.end_headers()
        self.wfile.write(jsdat)
        self.wfile.flush()
        codestore = []

def run(server_class=HTTPServer):
    server_address = ('127.0.0.1', 2468)
    httpd = server_class(server_address, Handler)
    httpd.serve_forever()

run()
