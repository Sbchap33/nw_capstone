import requests
import json
import yaml

url = "https://api.fivetran.com/v1/connectors/pampers_overnight/force"

conf = yaml.load(open('/home/ec2-user/environment/nw_capstone/API/Requirements.yml'))
basic = conf['key']['basic']

payload  = {}
headers = {
  'Authorization': basic,
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)

response.encoding= 'JSON'
r_json = json.loads(response.text)
r_dumps=json.dumps(r_json, indent=4)

print(r_dumps)