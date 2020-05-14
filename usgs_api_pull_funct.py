# Base API pull for USGS # 

import requests
import json
import flask
import logging

def main(request):
    try:
        #request = request.get_json() # handler method for flask object to Json
        # API specific inputs to function
        url = "https://waterservices.usgs.gov/nwis/iv/?format=json&sites=09058000&parameterCd=00060,00065&siteStatus=all"
        #Call the data function
        data = request_historical_data(url)
        state=data["time"]
        response = assemble_response_json(data,state)
        headers ={"Content-Type": "application/json"}
        return flask.make_response(response,200,headers)
        
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        

def request_historical_data(url_n):
    r = requests.request("GET", url_n)
    r.encoding= 'JSON'
    r_json = json.loads(r.text)
    r_dumps=json.dumps(r_json, indent=4)
    ######### date time ######## 
    time=r_json["value"]["queryInfo"]["note"][3]["value"]
    #update state with new time# 
    state=time
    #print(time)
    ########## site name ##########
    site_name=r_json["value"]["timeSeries"][0]["sourceInfo"]["siteName"]
    #print(site_name)
    ######### cfs ########
    cfs=r_json["value"]["timeSeries"][0]["values"][0]["value"][0]["value"]
    cfs=int(cfs)
    #print(cfs)
    ## organize into one tuple ## 
    data = {"time":time, "site_name":site_name, "cfs": cfs}
    data = data.json()
    return data
    #print(data)

######## function to organize response ###### 
def assemble_response_json(data_up, state_up):
    response_dict ={
        "state": {
            "upper_c": state_up
        },
        "insert": {
            "upper_c": data_up
        },
        "schema": {
            "upper_c": {
                "primary_key": ["time"]
            }
        },
        "hasMore": False
    }
    #print(json.dumps(response_dict))
    return json.dumps(response_dict)

main({
    "state": {
        "cursor": "2018-01-01T00:00:00Z"
    },
    "secrets": {
        "apiToken": "abcdefghijklmnopqrstuvwxyz_0123456789"
    }
})