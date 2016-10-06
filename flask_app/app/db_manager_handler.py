#!/usr/bin/python
import sys
import os
import requests
import json

db_manager_url_api = {
    "request":{
    "create_request_id": "/dbmanager/rest/request/"
    "check_status": "/dbmanager/rest/request/"
    },
    "user":{
    "create": "/dbmanager/rest/users/"
    "auth" : "/dbmanger/rest/users/auth"
    }
}


class Dbmanager:
	def __init__(self,root_url):
		self.root_url = root_url

	def get_request_id(request_type , request_parameters, result , request_status):
		required_url = self.root_url + db_manager_url_api["request"]["check_status"] + request_id
		data = {
  				"requestType": request_type,
                "requestStatus": request_status,
                "requestParameters":request_parameters
			}
		data_json = json.dumps(data)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		req_obj = requests.post(required_url , data = data_json , headers = headers )

	def request_check_status(request_id):
		required_url = self.root_url + db_manager_url_api["request"]["check_status"] + request_id
        req_obj = requests.get(required_url)

        if (req_obj.staus_code == 200) :
			req_obj_json = req_obj.json()
			data = {
				"requestId": requestId,
  				"requestType": req_obj_json["requestType"],
                "requestStatus": req_obj_json["requestStatus"],
                "requestParameters":req_obj_json["requestParameters"],
				"result" = req_obj_json["result"],
				"success" = True
			}
		elif (req_obj.staus_code == 404) :
			data = {
				"requestId": requestId,
				"result" = "Request Check Failed - Wrong Id",
				"success" = False
			}
			
		else :
			data = {
				"requestId": requestId,
				"result" = "Request Check Failed  - " + str(req_obj.text) ,
				"success" = False
			}
		resp_json = json.dumps(data)
		resp = Response(resp_json, status = req_obj.status_code, mimetype ='application/json')
		return resp


	def user_create(username,password):
		required_url = self.root_url + db_manager_url_api["user"]["create"]
		data = {
		"userName" : username
		"password" : password
		}
		data_json = json.dumps(data)
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		req_obj = requests.post(required_url , data = data_json , headers = headers )

		if (req_obj.staus_code == 201) :
			req_obj_json = req_obj.json()
			data = {
				"userId" = req_obj_json["userId"],
				"userName" = username,
				"result" = "User Created",
				"success" = True
			}
		elif (req_obj.staus_code == 400) :
			req_obj_json = req_obj.json()
			data = {
				"userId" = None,
				"userName" = username,
				"result" = "User Creation Failed - User Name Already Taken",
				"success" = False
			}
		else :
			data = {
				"userId" = None,
				"userName" = username,
				"result" = "User Creation Failed - " + str(req_obj.text) ,
				"success" = False
			}
		resp_json = json.dumps(data)
		resp = Response(resp_json, status=req_obj.status_code, mimetype='application/json')
		return resp


	def user_authenticate(username,password):
		required_url = db_manager_url + db_manager_url_api["user"]["auth"]
		data = {
		"userName" : username
		"password" : password
		}
		data_json = json.dumps(data)
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		req_obj = requests.post(required_url , data = data_json , headers = headers )



