import os
import requests
import random
import json
import ast

root_url = os.environ['ROOT_URL']
api_urls = ast.literal_eval(os.environ['API_URLS'])
request_id = os.environ['REQUEST_ID']
request_type = "create_user"
username = os.environ['USERNAME']
password = os.environ['PASSWORD']

def request_update( request_status, result):
    required_url = root_url + api_urls["request"]["update"]
    data = {
        "requestId": request_id,
        "requestType" : request_type,
        "requestStatus": request_status,
        "result" : result
    }
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    req_obj = requests.put(required_url, data = data_json, headers = headers)

    resp  = ( True if(req_obj.status_code == 200) else False )
    return resp

def user_create(username, password):
    username = username + "_" + str(random.randint(0,9999))
    required_url = root_url + api_urls["user"]["create"]
    data = {
        "userName": username,
        "password": password
    }
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    req_obj = requests.post(required_url, data = data_json, headers = headers)

    if req_obj.status_code == 201:
        req_obj_json = req_obj.json()
        data = {
            "userId": req_obj_json["userId"],
            "userName": username,
            "requestStatus": "User Created - Your userId is " + req_obj_json["userId"],
            "result": "success"
        }
    elif req_obj.status_code == 400:
        data = {
            "userId": None,
            "userName": username,
            "requestStatus": "User Creation Failed - User Name Already Taken",
            "result": "failure"
        }
    else:
        data = {
            "userId": None,
            "userName": username,
            "result": "User Creation Failed - " + str(req_obj.text),
            "result": "failure"
        }
    return data

if __name__ == "__main__":
    container_started_update = request_update("Container Spawned , Code To Be Executed", "in_progress")
    if container_started_update:
        resp_data = user_create(username, password)
        request_update(resp_data["requestStatus"], resp_data["result"])
    else:
        raise Exception("Fatal Exception - Request Update Failed")