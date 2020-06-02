import requests
import json

url = "https://waterservices.usgs.gov/nwis/iv/?format=json&sites=09058000&parameterCd=00060,00065&siteStatus=all"

payload  = {}
headers= {}

response = requests.request("GET", url, headers=headers, data = payload)

response.encoding= 'JSON'
r_json = json.loads(response.text)
r_dumps=json.dumps(r_json, indent=4)

print(r_dumps)
