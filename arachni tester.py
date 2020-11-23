import urllib.request as urllib2
import urllib
import json
import os
import time
from bs4 import BeautifulSoup

class ArachniClient(object):

   with open('./profiles/full_audit_normal.json') as f:
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
   
   def getScanReport(self, scanID, report_format):
      if report_format == 'html':
         report_format = 'html.zip'

      if report_format in ['json', 'xml', 'yaml','html.zip']:
         urllib.request.urlretrieve(self.arachni_url + "/scans/" + scanID + "/report." + report_format,"./reports/" + scanID + "." + report_format)
      elif report_format == None: #outputs to json by default
         urllib.request.urlretrieve(self.arachni_url + "/scans/" + scanID + "/report","./reports/" + scanID + ".json")
      else:
         print ("Your requested format is not available.")
   
   def processJSON(self, scanID):  
      with open("./reports/" + scanID + ".json", encoding="utf-8") as jsonfile:
         json_obj = json.load(jsonfile)

      try:
         for x in json_obj['issues']:
            print("Name: ",x['name'])
            print("Description: ",x['description'])
            print("Remedy guidance: ", x['remedy_guidance'])
            print("Issue found in site: ", x['vector']['url'])
            print("References: ", x['references'])
            print("")
      except Exception:
         pass
   
   def startAuthScan(self): #call this if user decides to do auth scan
      self.profile("./profiles/full_audit_auth.json")
      target_url = input("Enter URL: ")
      username = input("Input username: ")
      password = input("Input password: ")

      try:
         urllib2.urlopen(target_url)
         self.options["url"] = target_url
         self.options["plugins"]["autologin"]["url"] = target_url
         self.options["plugins"]["autologin"]["parameters"] = "email=" + username + "&" + "password=" + password
      except urllib2.HTTPError as e:
         print(e.code)


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#main
if __name__ == '__main__':
   #test website: http://testhtml5.vulnweb.com
   #test unpatched: http://cea1105f5552.ngrok.io/

   #init objects
   a = ArachniClient()
   resumeFlag = False
   authFlag = False
   
   #checks for existing scans and resumes from there instead
   avail_scan_object = a.get_scans() #returns json object of available scans
   print(a.get_scans()) #displays available scans | testing only

   for x in avail_scan_object: #check if avail scan is ongoing
      status_object = a.get_status(x)
      if(status_object["busy"] == True): #break and resume last scan if scan is still ongoing
         scan_ID = x
         resumeFlag = True
         start_time = time.time()
         break
   
   if(resumeFlag == False):
      checkAuth = input("Do you want to perform an Authenticated Scan? (y/n): ")
      while checkAuth not in ("y","n"):
         print("Invalid input")
         cls()
         checkAuth = input("Do you want to perform an Authenticated Scan? (y/n): ")

   #start new scan if there are no ongoing ones
   if(resumeFlag == False and checkAuth == "n"):
      print("Normal scan")
      url = input("Enter url: ")
      a.target(url)
      scan_json_object = a.start_scan() #outputs json dictionary
      scan_ID = scan_json_object["id"]
      start_time = time.time()

   elif(resumeFlag == False and checkAuth == "y"):
      authFlag = True
      print("Authenticated scan")
      a.startAuthScan()
      scan_json_object = a.start_scan() #outputs json dictionary
      scan_ID = scan_json_object["id"]
      start_time = time.time()

   while True:
      cls()
      print("Resumed scan? | ", resumeFlag)
      print("Authenticated? | ", authFlag)
      print("The scan is ongoing...")
      status_object = a.get_status(scan_ID)

      print("Current page is: ", status_object["statistics"]["current_page"])
      print("Total audited pages are: ", status_object["statistics"]["audited_pages"])
      print("Total found pages are: ", status_object["statistics"]["found_pages"])
      print("Elapsed time is: ", status_object["statistics"]["runtime"])
      print("Current status is: ", status_object["status"])
      print("Current busy flag is: ", status_object["busy"])

      if(status_object["busy"] == False):
         print("Total scan time: ", status_object["statistics"]["runtime"])
         print("Scan has been completed, retrieving report...")
         a.getScanReport(scan_ID,"json") #output to json for database processing
         a.getScanReport(scan_ID,"html") #output to html for user ease of interaction
         a.processJSON(scan_ID) #print out choice information
         break
      time.sleep(60) #delay status update to 1 minute per status request
      
   a.delete_scan(scan_ID) #comment this out if performing testing | deletes the scan after it is complete to prevent zombie processes