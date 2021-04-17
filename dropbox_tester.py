# #from mediafire.client import (MediaFireClient, File, Folder)
# from mediafire import (MediaFireApi, MediaFireUploader)
# from mediafire.client import (MediaFireClient, File, Folder)

# mediaFlag = False

# api = MediaFireApi()
# uploader = MediaFireUploader(api)
# session = api.user_get_session_token(email='fypemail@yahoo.com', password='iamusingastrongpassword', app_id='42511')

# client = MediaFireClient()
# client.login(email='fypemail@yahoo.com',
#     password='iamusingastrongpassword',
#     app_id='42511')

# # API client does not know about the token
# # until explicitly told about it:
# api.session = session
# scan_id = 'nolol2' #replace this part with the scanner id from the arachni scanner  
# response = api.user_get_info()
# print(response['user_info']['display_name']) #just testing

# client.upload_file('./reports/'+ scan_id + '.zip', "mf:/reports/")

# file_response = api.request("folder/get_content", {"folder_key":"tje4eo1vl6m83","content_type":"files"})
# print(file_response)
# file_object = file_response
# while(mediaFlag == False):
#     for item in file_object["folder_content"]["files"]:
#         print(item["filename"])
#         if(item["filename"] == scan_id + '.zip'):
#             print(item["links"]["normal_download"])
#             mediaFlag = True

# # fd = open('./reports/arachni_' + scan_id + '_scan_report.html.zip', 'rb')

# # result = uploader.upload(fd, 'arachni_' + scan_id + '_scan_report.html.zip',folder_key='tje4eo1vl6m83') #returns a json object

# # print(api.file_get_info(result.quickkey))
# # result_object = api.file_get_info(result.quickkey)
# # print(result_object["file_info"]["filename"])
# # print(result_object["file_info"]["links"]["normal_download"]) #returns the download link


# # print(client.download_file("mf:/reports/api_scan_report.html.zip","./reports/mediafiretest.zip"))

# import dropbox

# print("Init Dropbox API...")
# dbx = dropbox.Dropbox("ClkPn4pV_5sAAAAAAAAAAUm4ft1qOk4VNd77wioArPu7WbFxQBb1f7-UKZQPfaRB")

# print("Scanning for reports files...")
# result = dbx.files_list_folder(path="")
# print(result)


# scanID = "f1247dfee641c1a7ed953f5770bfd144"
# target = "/" + scanID + ".html.zip"
# filepath = "./reports/" + scanID + ".html.zip"

# with filepath.open("rb") as f:
#     meta = dbx.files_upload(f.read(), target, mode=dropbox.files.WriteMode("overwrite"))

import pathlib
import dropbox
import re

# the source file
folder = pathlib.Path("./reports/")    # located in this folder
scanID = "f1247dfee641c1a7ed953f5770bfd144"
filename = scanID + ".html.zip"         # file name
filepath = folder / filename  # path object, defining the file
print(filepath)

# target location in Dropbox
target = "/"              # the target folder
targetfile = target + filename   # the target path and file name

# Create a dropbox object using an API v2 key
d = dropbox.Dropbox("ClkPn4pV_5sAAAAAAAAAAUm4ft1qOk4VNd77wioArPu7WbFxQBb1f7-UKZQPfaRB")

print(d.users_get_current_account())

# open the file and upload it
with filepath.open("rb") as f:
   # upload gives you metadata about the file
   # we want to overwite any previous version of the file
   meta = d.files_upload(f.read(), targetfile, mode=dropbox.files.WriteMode("overwrite"))
   print(meta)

# create a shared link
link = d.sharing_create_shared_link(targetfile)

# url which can be shared
url = link.url

print(url)