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
user_id = os.environ['USER_ID']

request_data ={
    "root_url" : root_url,
    "api_url" : api_urls["request"]["update"],
    "request_id" : request_id,
    "request_type" : request_type
}

def user_delete(user_id):
    required_url = root_url + api_urls["user"]["delete"]
    delete_append_url = "/" + str(user_id)
    required_url = required_url + delete_append_url
    headers = {'Accept': 'text/plain'}
    request_obj = requests.delete(required_url,  headers = headers)

    if request_obj.status_code == 204:
        data = {
            "userId": user_id,
            "requestStatus": "User Deleted",
            "result": "success"
        }
    elif request_obj.status_code == 500:
        data = {
            "userId": user_id,
            "requestStatus": "User Deletion Failed - userId Not Present - " + str(request_obj.text),
            "result": "failure"
        }
    else:
        data = {
            "userId": None,
            "requestStatus": "User Deletion Failed - " + str(request_obj.text),
            "result": "failure"
        }
    return data

if __name__ == "__main__":
    container_started_update = request_update(request_data,status_codes[request_type][102], "in_progress")
    if container_started_update:
        response_data = user_delete(user_id)
        request_update(request_data, response_data["requestStatus"], response_data["result"])
    else:
        raise Exception("Fatal Exception - Request Update Failed")