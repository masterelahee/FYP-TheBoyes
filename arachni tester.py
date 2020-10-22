#!/usr/bin/env python

# see the documentation how to use more options in the JSON call
# https://github.com/Arachni/arachni/wiki/REST-API

import json
import urllib.request
from urllib.error import HTTPError

URL='http://unpatchedfyp.hopto.org'
SCAN_OPTS=['xss*','sql_injection*','csrf']
#SCAN_OPTS=['*'] # do every check

data = {
        'url': URL, 'checks' : SCAN_OPTS
}

f = urllib.parse.urlencode(data)
f = f.encode('utf-8')

req = urllib.request.Request('http://127.0.0.1:7331/scans')
req.add_header('Content-Type', 'application/json')

try:
    response = urllib.request.urlopen(req, f)
except HTTPError as e:
    content = e.read()