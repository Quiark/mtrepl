import os
import sys
import json
import time
import pdb
import readline
import threading

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen, Request

# TODO concurrency protection
codestore = []
results = []

class Handler(BaseHTTPRequestHandler):
    def log_request(self, code='', size=''):
        pass

    def do_GET(self):
        #pdb.set_trace()
        if self.path == '/code/add':
            self.add_code()
        elif self.path == '/code/get':
            self.get_code()
        elif self.path == '/response/add':
            self.add_response()
        elif self.path == '/response/get':
            self.get_response()
        else:
            self.wfile.write(b'nothing here')

    def read_json(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        return json.loads(body)

    def respond_json(self, obj):
        jsdat = json.dumps(obj).encode()

        self.send_response(200)
        self.send_header('content-type', 'application/json')
        self.send_header('content-length', len(jsdat))
        self.end_headers()
        self.wfile.write(jsdat)
        self.wfile.flush()

    def do_POST(self):
        return self.do_GET()

    def add_code(self):
        global codestore
        data = self.read_json()
        self.send_response(200)
        self.end_headers()

        # format check
        def require(p): 
            if not p: 
                print(data)
                raise RuntimeError('/code/add accepts {id: int, code: string}')
        require('id' in data)
        require('code' in data)

        codestore.append(data)

    def get_code(self):
        global codestore
        self.respond_json(codestore)
        codestore = []

    def get_response(self):
        global results
        self.respond_json(results)
        results = []

    def add_response(self):
        global results
        dat = self.read_json()
        if dat != None:
            if type(dat) is not list:
                print(dat)
                raise RuntimeError('Responses should be a list {id:, value:, error:}')
            if len(dat) > 0: print(dat)
            results += dat

        self.send_response(200)
        self.end_headers()

class CLI(threading.Thread):
    URL = 'http://127.0.0.1:2468'
    counter = 1

    def run(self):
        while True:
            self.one()

    def one(self):
        self.counter += 1
        code = input('> ')
        code = 'return ' + code   # otherwise Lua won't give us return value
        cmd = { 'code': code, 'id': self.counter }

        with urlopen(Request(self.URL + '/code/add', 
            headers={'Content-Type': 'application/json'},
            method='POST', 
            data=json.dumps(cmd).encode())) as resp:
                resp.read()

        # get response
        for ig in range(1000):
            with urlopen(Request(self.URL + '/response/get')) as r:
                resp = r.read()
                obj = json.loads(resp)
                found = False
                for it in obj:
                    if int(it['id']) == self.counter: 
                        if 'value' in it:
                            print(it['value'])
                        else:
                            print('ERROR', it['error'])
                        
                        found = True
                if found: break

            time.sleep(0.05)


def runserver(server_class=HTTPServer):
    server_address = ('127.0.0.1', 2468)
    httpd = server_class(server_address, Handler)
    httpd.serve_forever()

CLI().start()

runserver()
