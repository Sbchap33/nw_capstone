import requests
import json
import yaml

conf = yaml.load(open('/home/ec2-user/environment/nw_capstone/API/Requirements.yml'))
basic = conf['key']['basic']

url = "https://api.fivetran.com/v1/users/space_involve"
payload  = {}
headers = {
  'Authorization': basic
}

response = requests.request("GET", url, headers=headers, data = payload)

response.encoding= 'JSON'
r_json = json.loads(response.text)
r_dumps=json.dumps(r_json, indent=4)

print(r_dumps)