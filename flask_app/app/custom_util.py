#!/usr/bin/python
from flask import Flask, request, jsonify , json , Response
import docker
from db_manager_handler import dbm_api_urls , request_types
from constants import status_codes,container_image_names

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



def build_dict_with_base_data(swarm,db_manager_url,dbm_api_urls,faas_manager_url,faas_api_urls,status_codes):
    # data = dict(
    #             SWARM=swarm,
    #             DB_MANAGER_URL=db_manager_url,
    #             DBM_API_URLS = dbm_api_urls,
    #             FAAS_MANAGER_URL =faas_manager_url,
    #             FAAS_API_URLS=faas_api_urls,
    #             STATUS_CODES = status_codes
    data = dict(
        SWARM = swarm,
        DB_MANAGER_URL = db_manager_url,
        DBM_API_URLS = dbm_api_urls,
        FAAS_MANAGER_URL =faas_manager_url,
        FAAS_API_URLS=faas_api_urls
    )
    return data

def build_dict_with_request_data(docker_cont_or_serv_name,request_type,request_id):
    data = dict(
                CONT_OR_SERV_NAME=docker_cont_or_serv_name,
                REQUEST_TYPE=request_type,
                REQUEST_ID=request_id
            )
    return data
