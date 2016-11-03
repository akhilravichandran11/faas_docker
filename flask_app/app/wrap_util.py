#!/usr/bin/python
from functools import wraps
from flask import Flask, request, jsonify, json, Response
from db_manager_handler import Dbmanager , dbm_api_urls
from custom_util import build_response_for_missing_params,check_dict_for_mandatory_keys,check_dict_for_null_values
from constants import request_types,status_codes

def validate_auth(db_manager,request_type):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            resp = validate_auth_headers(request,db_manager,request_type)
            if resp:
                return resp
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator

def validate_auth_args(request,db_manager,request_type):
    resp = None
    request_args = request.args.to_dict(flat = True)
    required_arg_keys = ["userName", "password"]
    if not check_dict_for_mandatory_keys(request_args, required_arg_keys):
        resp = build_response_for_missing_params(request_types[request_type],required_arg_keys)
    else:
        respsone_data = db_manager.user_auth(request_args["userName"],request_args["password"])
        if not respsone_data["success"]:
            resp_data = {
                "result": request_types[request_type] + " Failed  - " + respsone_data["result"],
                "success": False
            }
            resp = Response(json.dumps(resp_data), status = 404, mimetype='application/json')
    return resp

def validate_auth_headers(request,db_manager,request_type):
    resp = None
    required_arg_keys = ["userName", "password"]
    user_name = request.headers.get("userName")
    password = request.headers.get("password")
    if (user_name is None) or (password is None):
        resp = build_response_for_missing_params(request_types[request_type],required_arg_keys)
    else:
        respsone_data = db_manager.user_auth(user_name,password)
        if not respsone_data["success"]:
            resp_data = {
                "result": request_types[request_type] + " Failed  - " + respsone_data["result"],
                "success": False
            }
            resp = Response(json.dumps(resp_data), status = 404, mimetype='application/json')
    return resp

def validate_arg_keys(request_type,required_arg_keys):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            resp = check_arg_keys(request,request_type,required_arg_keys)
            if resp:
                return resp
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator

def check_arg_keys(request,request_type,required_arg_keys):
    resp = None
    request_args = request.args.to_dict(flat = True)
    if not check_dict_for_mandatory_keys(request_args, required_arg_keys):
        resp =  build_response_for_missing_params(request_types[request_type],required_arg_keys)
    elif check_dict_for_null_values(request_args):
        resp_data = {
                "result": request_types[request_type] + " Failed  - " + "Parameters are Null Or Empty",
                "success": False
            }
        resp = Response(json.dumps(resp_data), status = 404, mimetype='application/json')
    return resp

