# Base API pull for USGS # 

import requests
import json
url = "https://waterservices.usgs.gov/nwis/iv/?format=json&sites=09058000&parameterCd=00060,00065&siteStatus=all"

r = requests.request("GET", url)
r.encoding= 'JSON'
r_json = json.loads(r.text)
r_dumps=json.dumps(r_json, indent=4)

######### date time ######## 
time=r_json["value"]["queryInfo"]["note"][3]["value"]

#update state with new time# 
state=time
print(time)

########## site name ##########
site_name=r_json["value"]["timeSeries"][0]["sourceInfo"]["siteName"]
print(site_name)

######### cfs ########
cfs=r_json["value"]["timeSeries"][0]["values"][0]["value"][0]["value"]
print(cfs)

## organize into one tuple ## 
#print(r_dumps)

######## functino to organize response ###### 
#def assemble_response_json(data,state):
#    insert = {"kremmling"}
#    response_dict ={
#        "state": state,
#        "schema": {
#            "upper_c": {
#                "primary_key": [
#                    "time"]
#            }
#        },
#        "insert": insert,
#        "hasMore": False
#    }
    #print(json.dumps(response_dict))
#    return json.dumps(response_dict)
    
#assemble_response_json()
