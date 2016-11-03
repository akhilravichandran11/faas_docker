#!/usr/bin/python
import requests
import json
import random
from flask import Response
from constants import request_types

dbm_api_urls = {
    "request": {
        "create": "/dbmanager/rest/request/",
        "update": "/dbmanager/rest/request/",
        "check_status": "/dbmanager/rest/request/"
    },
    "user": {
        "create": "/dbmanager/rest/users",
        "update": "/dbmanager/rest/users",
        "delete": "/dbmanager/rest/users",
        "auth": "/dbmanager/rest/users/auth",
        "get_id": "/dbmanager/rest/users/"
    },
    "function": {
        "get": "/dbmanager/rest/functions",
        "create": "/dbmanager/rest/functions",
        "update": "/dbmanager/rest/functions",
        "delete": "/dbmanager/rest/functions",
        "get_id": "/dbmanager/rest/functions"
    }
}


class Dbmanager:
    def __init__(self, root_url):
        self.root_url = root_url

    def request_create(self, request_type, request_parameters, request_status, result):
        if request_types.has_key(request_type):
            required_url = self.root_url + dbm_api_urls["request"]["create"]
            data = {
                "requestType": request_type,
                "requestStatus": request_status,
                "requestParameters": request_parameters,
                "result": result
            }
            data_json = json.dumps(data)
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            request_obj = requests.post(required_url, data=data_json, headers=headers)

            if request_obj.status_code == 201:
                request_obj_json = request_obj.json()
                data = {
                    "requestId": request_obj_json["requestId"],
                    "requestType": request_obj_json["requestType"],
                    "requestStatus": request_obj_json["requestStatus"],
                    "requestParameters": request_obj_json["requestParameters"],
                    "result": request_obj_json["result"],
                    "success": True
                }
            else:
                data = {
                    "requestId": None,
                    "requestType": request_type,
                    "requestStatus": request_status,
                    "requestParameters": request_parameters,
                    "result": "Create Request Failed  - " + str(request_obj.text),
                    "success": False
                }
            return data
        else:
            raise Exception("Invalid Request Type")

    def request_update(self, request_id, request_status):
        required_url = self.root_url + dbm_api_urls["request"]["update"]
        data = {
            "requestId": request_id,
            "requestStatus": request_status
        }
        data_json = json.dumps(data)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        request_obj = requests.put(required_url, data=data_json, headers=headers)

        if request_obj.status_code == 201:
            request_obj_json = request_obj.json()
            data = {
                "requestId": request_obj_json["requestId"],
                "requestType": request_obj_json["requestType"],
                "requestStatus": request_obj_json["requestStatus"],
                "requestParameters": request_obj_json["requestParameters"],
                "result": request_obj_json["result"],
                "success": True
            }
        else:
            data = {
                "requestId": request_id,
                "requestStatus": request_status,
                "result": "Update Request Failed  - " + str(request_obj.text),
                "success": False
            }
        resp_json = json.dumps(data)
        resp = Response(resp_json, status=request_obj.status_code, mimetype='application/json')
        return resp

    def request_check_status(self, request_id):
        required_url = self.root_url + dbm_api_urls["request"]["check_status"] + request_id
        request_obj = requests.get(required_url)

        if request_obj.status_code == 200:
            request_obj_json = request_obj.json()
            data = {
                "requestId": request_id,
                "requestType": request_obj_json["requestType"],
                "requestStatus": request_obj_json["requestStatus"],
                "requestParameters": request_obj_json["requestParameters"],
                "result": request_obj_json["result"],
                "success": True
            }
        elif request_obj.status_code == 404:
            data = {
                "requestId": request_id,
                "result": "Request Check Failed - request_id does not exist",
                "success": False
            }
        else:
            data = {
                "requestId": request_id,
                "result": "Request Check Failed  - " + str(request_obj.text),
                "success": False
            }
        resp_json = json.dumps(data)
        resp = Response(resp_json, status=request_obj.status_code, mimetype='application/json')
        return resp

    def user_auth(self, user_name, password):
        required_url = self.root_url + dbm_api_urls["user"]["auth"]
        data = {
            "userName": user_name,
            "password": password
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        request_obj = requests.post(required_url, data=json.dumps(data), headers=headers)
        if request_obj.status_code == 204:
            data = {
                "success": True,
                "result": "Login Succesfull"
            }
        elif request_obj.status_code == 400:
            data = {
                "success": False,
                "result": "Login Failure - Invalid Credentials"
            }
        else:
            data = {
                "success": False,
                "result": "Login Failure - " + " url - " + required_url + " - data - " + str(data) + "\n" + str(request_obj.text)
            }
        return data

    def user_get_id(self,user_name):
        required_url = self.root_url + dbm_api_urls["user"]["get_id"] + user_name
        headers = {'Accept': 'text/plain'}
        request_obj = requests.get(required_url, headers=headers)

        if request_obj.status_code == 200:
            request_obj_json = request_obj.json()
            data = {
                "userId": request_obj_json["userId"],
                "user_name": user_name,
                "requestStatus": "User Found",
                "result": "success",
                "success": True
            }
        elif request_obj.status_code == 404:
            data = {
                "userId": None,
                "user_name": user_name,
                "requestStatus": "User Not Found - " + str(request_obj.text),
                "result": "failure",
                "success": False
            }
        else:
            data = {
                "userId": None,
                "user_name": user_name,
                "requestStatus": "User Not Found - " + str(request_obj.text),
                "result": "failure",
                "success": False
            }
        return data

    def user_create(self, user_name, password):
        user_name = user_name + "_" + str(random.randint(0, 9999))
        required_url = self.root_url + dbm_api_urls["user"]["create"]
        data = {
            "userName": user_name,
            "password": password
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        request_obj = requests.post(required_url, data=json.dumps(data), headers=headers)

        if request_obj.status_code == 201:
            request_obj_json = request_obj.json()
            data = {
                "user_name": user_name,
                "requestStatus": "User Created - Your userId is " + request_obj_json["userId"],
                "result": "success"
            }
        elif request_obj.status_code == 400:
            data = {
                "userId": None,
                "user_name": user_name,
                "requestStatus": "User Creation Failed - User Name Already Taken " + str(request_obj.text),
                "result": "failure"
            }
        else:
            data = {
                "userId": None,
                "user_name": user_name,
                "requestStatus": "User Creation Failed - " + str(request_obj.text),
                "result": "failure"
            }
        resp = Response(json.dumps(data), status = request_obj.status_code, mimetype = 'application/json')
        return resp

    def user_update(self, user_id, user_name, password):
        required_url = self.root_url + dbm_api_urls["user"]["update"]
        data = {
            "userId" : user_id,
            "userName": user_name,
            "password": password
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        request_obj = requests.put(required_url, data=json.dumps(data), headers=headers)

        if request_obj.status_code == 200:
            request_obj_json = request_obj.json()
            data = {
                "userId": user_id,
                "user_name": request_obj_json["userName"],
                "requestStatus": "User Details Updated - Your userId is " + request_obj_json["userId"],
                "result": "success"
            }
        elif request_obj.status_code == 400:
            data = {
                "userId": user_id,
                "user_name": user_name,
                "requestStatus": "User Details Update Failed - User Name Already Taken " + str(request_obj.text),
                "result": "failure"
            }
        else:
            data = {
                "userId": user_id,
                "user_name": user_name,
                "requestStatus": "User Details Update Failed - " + str(request_obj.text),
                "result": "failure"
            }
        resp = Response(json.dumps(data), status = request_obj.status_code, mimetype = 'application/json')
        return resp

    def user_delete(self, user_id):
        required_url = self.root_url + dbm_api_urls["user"]["delete"]
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
        resp = Response(json.dumps(data), status=request_obj.status_code, mimetype='application/json')
        return resp

    def function_get_id(self,user_name,function_name):
        required_url = self.root_url + dbm_api_urls["function"]["get_id"] + "/" + user_name + "/" + function_name
        headers = {'Accept': 'text/plain'}
        request_obj = requests.get(required_url, headers=headers)

        if request_obj.status_code == 200:
            request_obj_json = request_obj.json()
            data = {
                "userId": request_obj_json["creator"]["userId"],
                "functionId": request_obj_json["functionId"],
                "requestStatus": "Function For User Found",
                "result": "success",
                "success": True
            }
        elif request_obj.status_code == 404:
            data = {
                "userId": None,
                "functionId": None,
                "requestStatus": "Function For User Not Found - " + str(request_obj.text),
                "result": "failure",
                "success": False
            }
        else:
            data = {
                "userId": None,
                "functionId": None,
                "requestStatus": "Function For User Not Found - " + str(request_obj.text),
                "result": "failure",
                "success": False
            }
        return data

    def function_create(self, function_name, function_content, user_id, user_name):
        function_name = function_name + "_" + str(random.randint(0, 9999))
        required_url = self.root_url + dbm_api_urls["function"]["create"]
        creator_data = {"userId": user_id, "userName": user_name}
        data = {"functionId": None,
                "functionName": function_name,
                "functionContent": function_content,
                "creator": creator_data
                }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        request_obj = requests.post(required_url, data=json.dumps(data), headers=headers)

        if request_obj.status_code == 201:
            request_obj_json = request_obj.json()
            data = {
                "functionId": request_obj_json["functionId"],
                "functionName": request_obj_json["functionName"],
                "functionContent": request_obj_json["functionContent"],
                "creator": {"userId": request_obj_json["creator"]["userId"],
                            "userName": request_obj_json["creator"]["userName"]},
                "requestStatus": "Function Created - Your functionId is " + request_obj_json["functionId"],
                "result": "success"
            }
        elif request_obj.status_code == 400:
            data = {
                "functionId": None,
                "functionName": function_name,
                "functionContent": function_content,
                "creator": creator_data,
                "requestStatus": "Function Creation Failed - Function Name Already Taken - " + str(request_obj.text),
                "result": "failure"
            }
        else:
            data = {
                "functionId": None,
                "functionName": function_name,
                "functionContent": function_content,
                "creator": creator_data,
                "requestStatus": "Function Creation Failed - " + str(request_obj.text),
                "result": "failure"
            }
        resp = Response(json.dumps(data), status=request_obj.status_code, mimetype='application/json')
        return resp

    def function_update(self, function_id, function_name, function_content, user_id, user_name):
        required_url = self.root_url + dbm_api_urls["function"]["update"]
        creator_data = {"userId": user_id, "userName": user_name}
        data = {"functionId": function_id,
                "functionName": function_name,
                "functionContent": function_content,
                "creator": creator_data
                }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        request_obj = requests.put(required_url, data=json.dumps(data), headers=headers)

        if request_obj.status_code == 200:
            request_obj_json = request_obj.json()
            data = {
                "functionId": request_obj_json["functionId"],
                "functionName": request_obj_json["functionName"],
                "functionContent": request_obj_json["functionContent"],
                "creator": {"userId": request_obj_json["creator"]["userId"],
                            "userName": request_obj_json["creator"]["userName"]},
                "requestStatus": "Function Updated - Your functionId is " + request_obj_json["functionId"],
                "result": "success"
            }
        elif request_obj.status_code == 400:
            data = {
                "functionId": function_id,
                "functionName": function_name,
                "functionContent": function_content,
                "creator": creator_data,
                "requestStatus": "Function Updated Failed - functionId Not Present - " + str(
                    request_obj.text),
                "result": "failure"
            }
        else:
            data = {
                "functionId": None,
                "functionName": function_name,
                "functionContent": function_content,
                "creator": creator_data,
                "requestStatus": "Function Update Failed - " + str(request_obj.text),
                "result": "failure"
            }
        resp = Response(json.dumps(data), status=request_obj.status_code, mimetype='application/json')
        return resp

    def function_delete(self, function_id):
        required_url = self.root_url + dbm_api_urls["function"]["delete"]
        delete_append_url = "/" + str(function_id)
        required_url = required_url + delete_append_url
        headers = {'Accept': 'text/plain'}
        request_obj = requests.delete(required_url,  headers = headers)

        if request_obj.status_code == 204:
            data = {
                "functionId": function_id,
                "requestStatus": "Function Deleted",
                "result": "success"
            }
        elif request_obj.status_code == 500:
            data = {
                "functionId": function_id,
                "requestStatus": "Function Deletion Failed - functionId Not Present - " + str(request_obj.text),
                "result": "failure"
            }
        else:
            data = {
                "functionId": None,
                "requestStatus": "Function Deletion Failed - " + str(request_obj.text),
                "result": "failure"
            }
        resp = Response(json.dumps(data), status=request_obj.status_code, mimetype='application/json')
        return resp

    def function_get(self, function_id):
        required_url = self.root_url + dbm_api_urls["function"]["get"]
        get_append_url = "/" + str(function_id)
        required_url = required_url + get_append_url
        headers = {'Accept': 'text/plain'}
        request_obj = requests.get(required_url,  headers = headers)

        if request_obj.status_code == 200:
            request_obj_json = request_obj.json()
            data = {
                "functionId": request_obj_json["functionId"],
                "functionName": request_obj_json["functionName"],
                "functionContent": request_obj_json["functionContent"],
                "requestStatus": "Function Found",
                "result": "success",
                "status_code" : request_obj.status_code,
                "success": True
            }
        elif request_obj.status_code == 404:
            data = {
                "functionId": function_id,
                "requestStatus": "Function Get Failed - functionId Not Present - " + str(request_obj.text),
                "result": "failure",
                "status_code": request_obj.status_code,
                "success": False
            }
        else:
            data = {
                "functionId": None,
                "requestStatus": "Function Get Failed - " + str(request_obj.text),
                "result": "failure",
                "status_code": request_obj.status_code,
                "success": False
            }
        return data