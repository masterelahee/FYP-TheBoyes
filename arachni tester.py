#!/usr/bin/env python

# see the documentation how to use more options in the JSON call
# https://github.com/Arachni/arachni/wiki/REST-API

import json
import urllib2
import subprocess

URL='http://testhtml5.vulnweb.com'
AUDIT_OPTS=['link', 'form', 'cookie', 'headers']
SCAN_OPTS=['xss*', 'sql_injection*', 'csrf']
#SCAN_OPTS=['*'] # do every check
IP=subprocess.check_output(["docker", "inspect", "-f", '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}', "webscanner"]).rstrip()
SCANNERURL="http://" + str(IP) + ":7331/scans"
data = {
        'url': URL, 'audit': {'elements': AUDIT_OPTS}, 'checks': SCAN_OPTS
}

req = urllib2.Request(SCANNERURL)
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(data))