# Base API pull for USGS # 

import requests
import json

def hello_world(request):
        url = "https://waterservices.usgs.gov/nwis/iv/?format=json&sites=09058000&parameterCd=00060,00065&siteStatus=all"
        payload = {}
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data = payload)
        json_data = json.loads(response.text)
        print(json_data)
