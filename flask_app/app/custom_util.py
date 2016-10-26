#!/usr/bin/python
from flask import Flask, request, jsonify , json , Response
import docker


def custom_print(obj, sepeartor='\n'):
    if type(obj) is dict:
        return custom_print_dict(obj, sepeartor)
    elif type(obj) is list:
        return custom_print_list(obj, sepeartor)
    else:
        return str(obj)

def custom_print_list(obj, sepeartor='\n'):
    final_string = []
    for current_item in obj:
        final_string.append(custom_print(current_item, sepeartor))
    final_string.append("*" * 10)
    return ("%s%s" % (sepeartor, sepeartor)).join(final_string)


def custom_print_dict(obj, sepeartor='\n'):
    final_string = []
    for key in obj:
        current_string = str(key) + " - " + custom_print(obj[key], sepeartor)
        final_string.append(current_string)
    final_string.append("#" * 10)
    return ("%s" % sepeartor).join(final_string)

def check_dict_for_mandatory_keys(check_dict,keys):
    present = set(keys).issubset(check_dict)
    return present

def build_response_for_missing_params(request_type,required_arg_keys):
    resp_data = {
        "result": request_type  + " Failed  - Required Parameters Missing - Required Parameters Are - " + str(required_arg_keys),
        "success": False
    }
    resp = Response(json.dumps(resp_data), status = 404, mimetype = 'application/json')
    return resp

def get_docker_logs_after_exit(docker_client , docker_container_name):
    while(docker_client.inspect_container(docker_container_name).get('State', dict()).get('Running')):
        print ""
    resp = "Container Name - " + docker_container_name + " \n Logs - " + docker_client.logs( docker_container_name, stdout = True, stderr = True, stream = False, timestamps = False)
    return resp
