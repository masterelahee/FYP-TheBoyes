import json

with open("./profiles/full_audit_auth.json", encoding="utf-8") as jsonfile:
         json_obj = json.load(jsonfile)

print(json_obj)
url = input("input URL: ")
username = input("Input username: ")
password = input("Input password: ")

json_obj["url"] = url
json_obj["plugins"]["autologin"]["url"] = url
json_obj["plugins"]["autologin"]["parameters"] = "email=" + username + "&" + "password=" + password

print(json_obj)

# try:
#     for x in json_obj['issues']:
#         print("Name: ",x['name'])
#         print("Description: ",x['description'])
#         print("Remedy guidance: ", x['remedy_guidance'])
#         print("Issue found in site: ", x['vector']['url'])
#         print("")
# except Exception:
#     pass