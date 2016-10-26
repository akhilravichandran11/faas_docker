import os
import requests
import random
import json
import ast
from util import request_update

root_url = os.environ['ROOT_URL']
api_urls = ast.literal_eval(os.environ['API_URLS'])
status_codes = ast.literal_eval(os.environ['STATUS_CODES'])
request_id = os.environ['REQUEST_ID']
request_type = os.environ['REQUEST_TYPE']
user_name = os.environ['USER_NAME']
password = os.environ['PASSWORD']

request_data ={
    "root_url" : root_url,
    "api_url" : api_urls["request"]["update"],
    "request_id" : request_id,
    "request_type" : request_type
}

def user_create(user_name, password):
    user_name = user_name + "_" + str(random.randint(0,9999))
    required_url = root_url + api_urls["user"]["create"]
    data = {
        "userNam": user_name,
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
    container_started_update = request_update(request_data,status_codes[request_type][102], "in_progress")
    if container_started_update:
        response_data = user_create(user_name, password)
        request_update(request_data, response_data["requestStatus"], response_data["result"])
    else:
        raise Exception("Fatal Exception - Request Update Failed")