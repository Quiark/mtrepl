import os
import sys
import json

from urllib.request import urlopen, Request

URL = 'http://127.0.0.1:2468'

while True:
    print('> ', end='')
    cmd = input()
    with urlopen(Request(URL + '/code/add', 
        headers={'Content-Type': 'application/json'},
        method='POST', 
        data=json.dumps(cmd).encode())) as resp:
            resp.read()

