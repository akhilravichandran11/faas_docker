#!/usr/bin/python
import requests
import json
from flask import Response

api_urls = {
	"request": {
		"create": "/dbmanager/rest/request/",
		"update": "/dbmanager/rest/request/",
		"check_status": "/dbmanager/rest/request/"
	},
	"user": {
		"create": "/dbmanager/rest/users/",
		"auth": "/dbmanger/rest/users/auth"
	}
}

request_types = {
	"create_user": "Create User",
	"create_function": "Create Function",
	"update_function": "Update Function",
	"execute_function": "Execute Function"
}


class Dbmanager:
	def __init__(self, root_url):
		self.root_url = root_url

	def request_create(self, request_type, request_parameters, request_status, result):
		if request_types.has_key(request_type):
			required_url = self.root_url + api_urls["request"]["create"]
			data = {
				"requestType": request_type,
				"requestStatus": request_status,
				"requestParameters": request_parameters,
				"result" : result
			}
			data_json = json.dumps(data)
			headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
			req_obj = requests.post(required_url, data = data_json, headers = headers)

			if req_obj.status_code == 201:
				req_obj_json = req_obj.json()
				data = {
					"requestId": req_obj_json["requestId"],
					"requestType": req_obj_json["requestType"],
					"requestStatus": req_obj_json["requestStatus"],
					"requestParameters": req_obj_json["requestParameters"],
					"result": req_obj_json["result"],
					"success": True
				}
			else:
				data = {
					"requestId": None,
					"requestType": request_type,
					"requestStatus": request_status,
					"requestParameters": request_parameters,
					"result": "Create Request Failed  - " + str(req_obj.text),
					"success": False
				}
			return data
		else:
			raise Exception("Invalid Request Type")

	def request_update(self, request_id, request_status):
		required_url = self.root_url + api_urls["request"]["update"]
		data = {
			"requestId": request_id,
			"requestStatus": request_status
		}
		data_json = json.dumps(data)
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		req_obj = requests.put(required_url, data = data_json, headers = headers)

		if req_obj.status_code == 201:
			req_obj_json = req_obj.json()
			data = {
				"requestId": req_obj_json["requestId"],
				"requestType": req_obj_json["requestType"],
				"requestStatus": req_obj_json["requestStatus"],
				"requestParameters": req_obj_json["requestParameters"],
				"result": req_obj_json["result"],
				"success": True
			}
		else:
			data = {
				"requestId": request_id,
				"requestStatus": request_status,
				"result": "Update Request Failed  - " + str(req_obj.text),
				"success": False
			}
		resp_json = json.dumps(data)
		resp = Response(resp_json, status = req_obj.status_code, mimetype = 'application/json')
		return resp

	def request_check_status(self, request_id):
		required_url = self.root_url + api_urls["request"]["check_status"] + request_id
		req_obj = requests.get(required_url)

		if req_obj.status_code == 200:
			req_obj_json = req_obj.json()
			data = {
				"requestId": request_id,
				"requestType": req_obj_json["requestType"],
				"requestStatus": req_obj_json["requestStatus"],
				"requestParameters": req_obj_json["requestParameters"],
				"result": req_obj_json["result"],
				"success": True
			}
		elif req_obj.status_code == 404:
			data = {
				"requestId": request_id,
				"result": "Request Check Failed - request_id does not exist",
				"success": False
			}
		else:
			data = {
				"requestId": request_id,
				"result": "Request Check Failed  - " + str(req_obj.text),
				"success": False
			}
		resp_json = json.dumps(data)
		resp = Response(resp_json, status=req_obj.status_code, mimetype='application/json')
		return resp

		# def user_authenticate(self, username, password):
		#     required_url = db_manager_url + api_urls["user"]["auth"]
		#     data = {
		#         "userName": username,
		#         "password": password
		#     }
		#     data_json = json.dumps(data)
		#     headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		#     req_obj = requests.post(required_url, data=data_json, headers=headers)
