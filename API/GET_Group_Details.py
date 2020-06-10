import requests
import json
import yaml

url = "https://api.fivetran.com/v1/groups/{group id}/connectors"

conf = yaml.load(open('{User Directory}/Requirements.yml'))
basic = conf['key']['basic']

payload  = {}
headers = {
  'Authorization': basic
}

response = requests.request("GET", url, headers=headers, data = payload)

response.encoding= 'JSON'
r_json = json.loads(response.text)
r_dumps=json.dumps(r_json, indent=4)

print(r_dumps)
