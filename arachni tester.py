# #!/usr/bin/env python

# # see the documentation how to use more options in the JSON call
# # https://github.com/Arachni/arachni/wiki/REST-API

# import json
# import urllib.request
# from urllib.error import HTTPError

# URL='https://juice-shop.herokuapp.com/'
# #SCAN_OPTS=['xss*','sql_injection*','csrf']
# SCAN_OPTS=['*'] # do every check

# data = {
#         'url': URL, 'checks' : SCAN_OPTS
# }

# f = urllib.parse.urlencode(data)
# f = f.encode('utf-8') #encode data dict before opening the url

# req = urllib.request.Request('http://127.0.0.1:7331/scans') #contact arachni rest server on local machine
# req.add_header('Content-Type', 'application/json')

# response = urllib.request.urlopen(req, f)

# # try:
# #     response = urllib.request.urlopen(req, f)
# # except HTTPError as e:
# #     content = e.read() #read error response

import urllib.request as urllib2
import urllib
import json
import os
import time
from bs4 import BeautifulSoup

class ArachniClient(object):

   with open('./profiles/speedscan.json') as f:
      default_profile = json.load(f)

   def __init__(self, arachni_url = 'http://127.0.0.1:7331'):
      self.arachni_url = arachni_url
      self.options = ArachniClient.default_profile

   def get_http_request(self, api_path):
      return urllib2.urlopen(self.arachni_url + api_path).read()

   def post_api(self, api_path):
      options = json.dumps(self.options).encode("utf-8")
      request = urllib2.Request(self.arachni_url + api_path, options)
      request.add_header('Content-Type', 'application/json')
      return urllib2.urlopen(request).read()

   def put_request(self, api_path):
      request = urllib2.Request(self.arachni_url + api_path)
      request.get_method = lambda: 'PUT'
      return urllib2.urlopen(request).read()

   def delete_request(self, api_path):
      request = urllib2.Request(self.arachni_url + api_path)
      request.get_method = lambda: 'DELETE'
      return urllib2.urlopen(request).read()
      
   def get_scans(self):
      return json.loads(self.get_http_request('/scans'))

   def get_status(self, scan_id):
      return json.loads(self.get_http_request('/scans/' + scan_id))

   def pause_scan(self, scan_id):
      return self.put_request('/scans/' + scan_id + '/pause')

   def resume_scan(self, scan_id):
      return self.put_request('/scans/' + scan_id + '/resume')

   def get_report(self, scan_id, report_format = None):
      if self.get_status(scan_id)['status'] == 'done':

         if report_format == 'html':
            report_format = 'html.zip'

         if report_format in ['json', 'xml', 'yaml', 'html.zip']:
            return self.get_http_request('/scans/' + scan_id + '/report.' + report_format)
         elif report_format == None:
            return self.get_http_request('/scans/' + scan_id + '/report')
         else:
            print ('your requested format is not available.')

      else:
         print('your requested scan is in progress.')

   def delete_scan(self, scan_id):
      return self.delete_request('/scans/' + scan_id)

   def start_scan(self):
      if self.options['url']:
         return json.loads(self.post_api('/scans')) #returns a dictionary
      else:
         print('Target is not set!')

   def target(self, target_url):
      try:
         urllib2.urlopen(target_url)
         self.options['url'] = target_url
      except urllib2.HTTPError as e:
         print(e.code)

   def profile(self, profile_path):
      with open(profile_path) as f:
         self.options = json.load(f)

   
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

if __name__ == '__main__':
   a = ArachniClient()

   url = input("Enter url: ")
   a = ArachniClient()
   a.target(url)
   scan_json_object = a.start_scan() #outputs json dictionary
   scan_ID = scan_json_object["id"]
   start_time = time.time()
   #print(scan_ID) #in case program fails and scans need to be terminated again
   while True:
      cls()
      print("scan is ongoing")
      status_object = a.get_status(scan_ID)
      print(status_object["status"])
      print(status_object["issues"])
      print(status_object["busy"])
      if(status_object["busy"] == False):
         print("Scan has been completed, retrieving report...")
         urllib.request.urlretrieve("http://127.0.0.1:7331/scans/" + scan_ID + "/report.xml","arachni_" + scan_ID + "_scan_report.xml") #sends a call for report after scan is complete
         #beautify xml output
         bs = BeautifulSoup(open("arachni_" + scan_ID + "_scan_report.xml"),"xml")
         xml_output = bs.prettify()
         with open("pretty_xml_report_" + scan_ID + ".xml", "w") as f:
            f.write(xml_output)
         print("Elapsed time is: ", time.time() - start_time)
         break
      time.sleep(60)
      
   a.delete_scan(scan_ID)
   a.delete_scan("5d059285b09c565cb5c8e5a5af25b2d0")