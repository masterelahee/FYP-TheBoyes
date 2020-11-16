from mediafire.client import (MediaFireClient, File, Folder)
from mediafire import MediaFireApi

api = MediaFireApi()
session = api.user_get_session_token(email='fypemail@yahoo.com', password='iamusingastrongpassword', app_id='42511')

# API client does not know about the token
# until explicitly told about it:
api.session = session
scan_id = '1e82a339b6dae6aaa4c3c08f605456d5'
response = api.user_get_info()
print(response['user_info']['display_name'])
file_response = api.request("folder/get_content", {"folder_key":"tje4eo1vl6m83","content_type":"files"})
print(file_response)
file_object = file_response
for item in file_object["folder_content"]["files"]:
    print(item["filename"])
    if(item["filename"] == "arachni_" + scan_id + "_scan_report.html.zip"):
        print(item["links"]["normal_download"])
# client = MediaFireClient()
# client.login(email='fypemail@yahoo.com',
#     password='iamusingastrongpassword',
#     app_id='42511')

# #client.upload_file("./reports/api_scan_report.html.zip", "mf:/reports/")
# print(client.download_file("mf:/reports/api_scan_report.html.zip","./reports/mediafiretest.zip"))
