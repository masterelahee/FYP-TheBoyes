#from mediafire.client import (MediaFireClient, File, Folder)
from mediafire import (MediaFireApi, MediaFireUploader)

api = MediaFireApi()
uploader = MediaFireUploader(api)
session = api.user_get_session_token(email='fypemail@yahoo.com', password='iamusingastrongpassword', app_id='42511')

# API client does not know about the token
# until explicitly told about it:
api.session = session
scan_id = 'c986268b91939398f29378ee3f111c2e' #replace this part with the scanner id from the arachni scanner  
response = api.user_get_info()
print(response['user_info']['display_name']) #just testing

# file_response = api.request("folder/get_content", {"folder_key":"tje4eo1vl6m83","content_type":"files"})
# print(file_response)
# file_object = file_response
# for item in file_object["folder_content"]["files"]:
#     print(item["filename"])
#     if(item["filename"] == "arachni_" + scan_id + "_scan_report.html.zip"):
#         print(item["links"]["normal_download"])

fd = open('./reports/arachni_' + scan_id + '_scan_report.html.zip', 'rb')

result = uploader.upload(fd, 'arachni_' + scan_id + '_scan_report.html.zip',folder_key='tje4eo1vl6m83') #returns a json object

print(api.file_get_info(result.quickkey))
result_object = api.file_get_info(result.quickkey)
print(result_object["file_info"]["filename"])
print(result_object["file_info"]["links"]["normal_download"]) #returns the download link

# client = MediaFireClient()
# client.login(email='fypemail@yahoo.com',
#     password='iamusingastrongpassword',
#     app_id='42511')

# #client.upload_file("./reports/api_scan_report.html.zip", "mf:/reports/")
# print(client.download_file("mf:/reports/api_scan_report.html.zip","./reports/mediafiretest.zip"))
