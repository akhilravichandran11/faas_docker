import requests
import json

def request_update( request_data, request_status, result, request_parameters = None ):
    required_url = request_data["db_manager_url"] + request_data["api_url"]
    data = {
        "requestId": request_data["request_id"],
        "requestType" : request_data["request_type"],
        "requestStatus": request_status,
        "result" : result
    }
    if request_parameters is not None:
        data.update({"requestParameters" : request_parameters})
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    request_obj = requests.put(required_url, data = json.dumps(data), headers = headers)

    response  = ( True if(request_obj.status_code == 200) else False )
    return response

def faas_remove_service(faas_manager_url,api_url,cont_or_serv_name):
    delete_append_url = "/" + str(cont_or_serv_name)
    required_url = faas_manager_url + api_url + delete_append_url
    headers = { 'Accept': 'text/plain'}
    request_obj = requests.delete(required_url, headers = headers)
    response  = ( True if(request_obj.status_code == 200) else False )
    return response

def cont_or_serv_remove_logic( swarm , faas_manager_data):
    if swarm:
        faas_remove_service(faas_manager_data["faas_manager_url"],faas_manager_data["faas_api_urls"]["service"]["remove"],faas_manager_data["cont_or_serv_name"])
        while (True):
            pass