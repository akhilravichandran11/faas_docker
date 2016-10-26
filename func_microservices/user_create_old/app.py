import os
import requests
import random
import json
import ast

root_url = os.environ['ROOT_URL']
api_urls = ast.literal_eval(os.environ['API_URLS'])
request_id = os.environ['REQUEST_ID']
request_type = "create_user"
user_name = os.environ['USER_NAME']
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
    request_obj = requests.put(required_url, data = data_json, headers = headers)

    response  = ( True if(request_obj.status_code == 200) else False )
    return response

def user_create(user_name, password):
    user_name = user_name + "_" + str(random.randint(0,9999))
    required_url = root_url + api_urls["user"]["create"]
    data = {
        "userName": user_name,
        "password": password
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    request_obj = requests.post(required_url, data = json.dumps(data), headers = headers)

    if request_obj.status_code == 201:
        request_obj_json = request_obj.json()
        data = {
            "userId": request_obj_json["userId"],
            "userName": user_name,
            "requestStatus": "User Created - Your userId is " + request_obj_json["userId"],
            "result": "success"
        }
    elif request_obj.status_code == 400:
        data = {
            "userId": None,
            "userName": user_name,
            "requestStatus": "User Creation Failed - User Name Already Taken",
            "result": "failure"
        }
    else:
        data = {
            "userId": None,
            "userName": user_name,
            "requestStatus": "User Creation Failed - " + str(request_obj.text),
            "result": "failure"
        }
    return data

if __name__ == "__main__":
    container_started_update = request_update("Container Spawned , Code To Be Executed", "in_progress")
    if container_started_update:
        response_data = user_create(user_name, password)
        request_update(response_data["requestStatus"], response_data["result"])
    else:
        raise Exception("Fatal Exception - Request Update Failed")