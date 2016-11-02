import os
import requests
import random
import json
import ast
from util import request_update,cont_or_serv_remove_logic
from func_exec import execute_function

swarm = ast.literal_eval(os.environ['SWARM'])
db_manager_url = os.environ['DB_MANAGER_URL']
dbm_api_urls = ast.literal_eval(os.environ['DBM_API_URLS'])
faas_manager_url = os.environ['FAAS_MANAGER_URL']
faas_api_urls = ast.literal_eval(os.environ['FAAS_API_URLS'])
status_codes = ast.literal_eval(os.environ['STATUS_CODES'])
cont_or_serv_name = os.environ['CONT_OR_SERV_NAME']
request_id = os.environ['REQUEST_ID']
request_type = os.environ['REQUEST_TYPE']
function_content = os.environ['FUNCTION_CONTENT']
function_input = os.environ['FUNCTION_INPUT']
function_output = os.environ['FUNCTION_OUTPUT']

request_data ={
    "db_manager_url" : db_manager_url,
    "api_url" : dbm_api_urls["request"]["update"],
    "request_id" : request_id,
    "request_type" : request_type
}

faas_manager_data ={
    "faas_manager_url" : faas_manager_url,
    "faas_api_urls" : faas_api_urls,
    "cont_or_serv_name" : cont_or_serv_name
}

def function_execute(function_content, function_output,function_input):
    func_data = execute_function(function_content, function_output, function_input)
    return func_data


if __name__ == "__main__":
    container_started_update = request_update(request_data,status_codes[request_type][102], "in_progress")
    if container_started_update:
        func_data = function_execute(function_content, function_output,function_input)
        request_update(request_data, func_data["requestStatus"], func_data["result"] , func_data["outputData"])
        cont_or_serv_remove_logic( swarm , faas_manager_data)
    else:
        raise Exception("Fatal Exception - Request Update Failed")