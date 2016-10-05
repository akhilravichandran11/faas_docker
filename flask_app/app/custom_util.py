#!/usr/bin/python
import sys
import os
import requests
import json

def custom_print(obj,sepeartor = '\n'):
	if type(obj) is dict:
		return custom_print_dict(obj,sepeartor)
	elif type(obj) is list:
		return custom_print_list(obj,sepeartor)
	else:
		return str(obj)

def custom_print_list(obj,sepeartor = '\n'):
	final_string = []
	for current_item in obj:
		final_string.append(custom_print(current_item,sepeartor))
	final_string.append("*"*10)
	return ("%s%s" % (sepeartor,sepeartor)).join(final_string)

def custom_print_dict(obj,sepeartor = '\n'):
	final_string = []
	for key in obj:
		current_string = str(key) + " - " + custom_print(obj[key],sepeartor)
		final_string.append(current_string)
	final_string.append("#"*10)
	return ("%s" % sepeartor).join(final_string)

def return_request_response(request_obj):
	response_json = None
	if request_obj.status_code == 200 && request_obj.json() is not None :
		response_json = request_obj.json()
	else :
		data = {
			"json_data" : None
		}
		response_json = json.dumps(data)
	resp = Response(response_json, status=request_obj.status_code, mimetype='application/json')
	return resp
