import json

json_file = open('./reports/arachni_36e1b4394b8c82c469a2ccdab037771e_scan_report.json')

json_obj = json.load(json_file)

try:
    for x in json_obj['issues']:
        print("Name: ",x['name'])
        print("Description: ",x['description'])
        print("Remedy guidance: ", x['remedy_guidance'])
        print("Issue found in site: ", x['vector']['url'])
        print("")
except Exception:
    pass
