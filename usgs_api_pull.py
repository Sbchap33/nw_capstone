# Base API pull for USGS # 

import requests
import json
url = "https://waterservices.usgs.gov/nwis/iv/?format=json&sites=09058000&parameterCd=00060,00065&siteStatus=all"

r = requests.request("GET", url)
r.encoding= 'JSON'
r_json = json.loads(r.text)
r_dumps=json.dumps(r_json, indent=4)

def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results

print(r_dumps)

######### cfs ########
cfs=r_json["value"]["timeSeries"][0]["values"][0]["value"][0]["value"]
print(cfs)

########## site name ##########

#site_name=r_json["value"]["timeSeries"][0]["sourceInfo"]["siteName"]
#print(site_name)

