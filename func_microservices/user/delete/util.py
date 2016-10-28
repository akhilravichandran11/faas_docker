import requests
import json

def request_update( request_data, request_status, result):
    required_url = request_data["db_manager_url"] + request_data["api_url"]
    data = {
        "requestId": request_data["request_id"],
        "requestType" : request_data["request_type"],
        "requestStatus": request_status,
        "result" : result
    }
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    request_obj = requests.put(required_url, data = data_json, headers = headers)

    response  = ( True if(request_obj.status_code == 200) else False )
    return response