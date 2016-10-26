from flask import Flask, request, jsonify , json , Response
import docker
import requests
import json
import traceback
import random
import datetime


import custom_util
from db_manager_handler import Dbmanager , api_urls , request_types
from constants import status_codes

app = Flask(__name__)

#  URLS for talking to docker containers
db_manager_link_url = "http://dbmanager:8080"
# db_manager_url = "http://" + socket.gethostbyname(socket.gethostname()) + ":8080"
db_manager_url = "http://0.0.0.0:8080"

#  Objects Initiated for lifecycle of flask app
docker_client = docker.Client(base_url='unix://var/run/docker.sock')
dbmanager = Dbmanager(db_manager_url)
dt_now = datetime.datetime.now()

@app.route("/")
def hello():
    return "Welcome To Madhatterz - FAAS"


@app.route("/request/check_status", methods = ['GET'] )
def request_check_status():
    request_type = 'request_status'
    required_arg_keys = ["requestId"]
    try:
        request_args = request.args.to_dict(flat = True)
        if custom_util.check_dict_for_mandatory_keys(request_args, required_arg_keys):
            resp = dbmanager.request_check_status(request_args["requestId"])
        else:
            resp = custom_util.build_response_for_missing_params(request_types[request_type], required_arg_keys)
    except Exception as e:
        resp = traceback.format_exc()
    return resp


@app.route("/user/create", methods = ['POST'] )
def user_create():
    request_type = 'create_user'
    required_arg_keys = ["userName", "password"]
    docker_image_name = 'cc_user_create'
    docker_container_name = docker_image_name + dt_now.strftime('_cont_%m.%d.%Y_') + str(random.randint(0,9999))
    try:
        request_args = request.args.to_dict(flat = True)
        if custom_util.check_dict_for_mandatory_keys(request_args, required_arg_keys):
            response_data = dbmanager.request_create(request_type, json.dumps(request_args), status_codes[request_type][101], "in_progress")
            resp = Response(json.dumps(response_data), status = 200, mimetype = 'application/json' )
            if response_data["success"]:
                data = {
                    "ROOT_URL" : db_manager_url,
                    "API_URLS" : api_urls,
                    "STATUS_CODES": status_codes,
                    "REQUEST_ID" : response_data["requestId"],
                    "REQUEST_TYPE" : request_type,
                    "USER_NAME" : request_args["userName"],
                    "PASSWORD": request_args["password"]
                }
                # resp = dbmanager.user_create(data["USER_NAME"], data["PASSWORD"])
                host_config = docker_client.create_host_config(privileged = False, network_mode = 'host')
                current_container = docker_client.create_container(image = docker_image_name  , name = docker_container_name , environment = data , host_config = host_config)
                docker_client.start(current_container)
            else:
                resp = custom_util.build_response_for_missing_params(request_types[request_type],required_arg_keys)
    except Exception as e:
        resp = traceback.format_exc()
    return resp

@app.route("/user/update", methods = ['PUT'] )
def user_update():
    request_type = 'update_user'
    required_arg_keys = ["userId","userName", "password"]
    docker_image_name = 'cc_user_update'
    docker_container_name = docker_image_name + dt_now.strftime('_cont_%m.%d.%Y_') + str(random.randint(0,9999))
    try:
        request_args = request.args.to_dict(flat = True)
        if custom_util.check_dict_for_mandatory_keys(request_args, required_arg_keys):
            response_data = dbmanager.request_create(request_type, json.dumps(request_args), status_codes[request_type][101], "in_progress")
            resp = Response(json.dumps(response_data), status = 200, mimetype = 'application/json' )
            if response_data["success"]:
                data = {
                    "ROOT_URL" : db_manager_url,
                    "API_URLS" : api_urls,
                    "STATUS_CODES" : status_codes,
                    "REQUEST_ID" : response_data["requestId"],
                    "REQUEST_TYPE" : request_type,
                    "USER_ID": request_args["userId"],
                    "USER_NAME" : request_args["userName"],
                    "PASSWORD": request_args["password"]
                }
                resp = dbmanager.user_update(data["USER_ID"],data["USER_NAME"],data["PASSWORD"])
                # host_config = docker_client.create_host_config(privileged = False, network_mode = 'host')
                # current_container = docker_client.create_container(image = docker_image_name  , name = docker_container_name , environment = data , host_config = host_config)
                # docker_client.start(current_container)
            else:
                resp = custom_util.build_response_for_missing_params(request_types[request_type],required_arg_keys)
    except Exception as e:
        resp = traceback.format_exc()
    return resp

@app.route("/user/delete" , methods = ['DELETE'] )
def user_delete():
    request_type = 'delete_user'
    required_arg_keys = ["userName","password","userId"]
    docker_image_name = 'cc_user_delete'
    docker_container_name = docker_image_name + dt_now.strftime('_cont_%m.%d.%Y_') + str(random.randint(0, 9999))
    try:
        request_args = request.args.to_dict(flat = True)
        if custom_util.check_dict_for_mandatory_keys(request_args,required_arg_keys):
            response_data = dbmanager.request_create(request_type, json.dumps(request_args),status_codes[request_type][101], "in_progress")
            resp = Response(json.dumps(response_data), status = 200, mimetype = 'application/json' )
            if response_data["success"]:
                data = {
                    "ROOT_URL": db_manager_url,
                    "API_URLS": api_urls,
                    "REQUEST_ID": response_data["requestId"],
                    "REQUEST_TYPE": request_type,
                    "USER_ID": request_args["userId"]
                }
                resp = dbmanager.user_delete(data["USER_ID"])
                # host_config = docker_client.create_host_config(privileged = False, network_mode = 'host')
                # current_container = docker_client.create_container(image = docker_image_name  , name = docker_container_name , environment = data , host_config = host_config)
                # docker_client.start(current_container)
        else:
            resp = custom_util.build_response_for_missing_params(request_types[request_type], required_arg_keys)
    except Exception as e:
        resp = traceback.format_exc()
    return resp


@app.route("/function/create" , methods = ['POST'] )
def function_create():
    request_type = 'create_function'
    required_arg_keys = ["userId", "userName","password","functionName"]
    docker_image_name = 'cc_function_create'
    docker_container_name = docker_image_name + dt_now.strftime('_cont_%m.%d.%Y_') + str(random.randint(0, 9999))
    try:
        request_args = request.args.to_dict(flat = True)
        if custom_util.check_dict_for_mandatory_keys(request_args,required_arg_keys):
            response_data = dbmanager.request_create(request_type, json.dumps(request_args),status_codes[request_type][101], "in_progress")
            resp = Response(json.dumps(response_data), status = 200, mimetype = 'application/json' )
            if response_data["success"]:
                data = {
                    "ROOT_URL": db_manager_url,
                    "API_URLS": api_urls,
                    "REQUEST_ID": response_data["requestId"],
                    "REQUEST_TYPE": request_type,
                    "USER_ID" : request_args["userId"],
                    "USER_NAME": request_args["userName"],
                    "FUNCTION_NAME" : request_args["functionName"],
                    "FUNCTION_CONTENT" : request.data
                }
                resp = dbmanager.function_create(data["FUNCTION_NAME"],data["FUNCTION_CONTENT"],data["USER_ID"],data["USER_NAME"])
                # host_config = docker_client.create_host_config(privileged = False, network_mode = 'host')
                # current_container = docker_client.create_container(image = docker_image_name  , name = docker_container_name , environment = data , host_config = host_config)
                # docker_client.start(current_container)
        else:
            resp = custom_util.build_response_for_missing_params(request_types[request_type], required_arg_keys)
    except Exception as e:
        resp = traceback.format_exc()
    return resp

@app.route("/function/update" , methods = ['PUT'] )
def function_update():
    request_type = 'update_function'
    required_arg_keys = ["userId", "userName","password","functionName","functionId"]
    docker_image_name = 'cc_function_update'
    docker_container_name = docker_image_name + dt_now.strftime('_cont_%m.%d.%Y_') + str(random.randint(0, 9999))
    try:
        request_args = request.args.to_dict(flat = True)
        if custom_util.check_dict_for_mandatory_keys(request_args,required_arg_keys):
            response_data = dbmanager.request_create(request_type, json.dumps(request_args),status_codes[request_type][101], "in_progress")
            resp = Response(json.dumps(response_data), status = 200, mimetype = 'application/json' )
            if response_data["success"]:
                data = {
                    "ROOT_URL": db_manager_url,
                    "API_URLS": api_urls,
                    "REQUEST_ID": response_data["requestId"],
                    "REQUEST_TYPE": request_type,
                    "USER_ID" : request_args["userId"],
                    "USER_NAME": request_args["userName"],
                    "FUNCTION_ID": request_args["functionId"],
                    "FUNCTION_NAME" : request_args["functionName"],
                    "FUNCTION_CONTENT" : request.data
                }
                resp = dbmanager.function_update(data["FUNCTION_ID"],data["FUNCTION_NAME"],data["FUNCTION_CONTENT"],data["USER_ID"],data["USER_NAME"])
                # host_config = docker_client.create_host_config(privileged = False, network_mode = 'host')
                # current_container = docker_client.create_container(image = docker_image_name  , name = docker_container_name , environment = data , host_config = host_config)
                # docker_client.start(current_container)
        else:
            resp = custom_util.build_response_for_missing_params(request_types[request_type], required_arg_keys)
    except Exception as e:
        resp = traceback.format_exc()
    return resp

@app.route("/function/delete" , methods = ['DELETE'] )
def function_delete():
    request_type = 'delete_function'
    required_arg_keys = ["userName","password","functionId"]
    docker_image_name = 'cc_function_delete'
    docker_container_name = docker_image_name + dt_now.strftime('_cont_%m.%d.%Y_') + str(random.randint(0, 9999))
    try:
        request_args = request.args.to_dict(flat = True)
        if custom_util.check_dict_for_mandatory_keys(request_args,required_arg_keys):
            response_data = dbmanager.request_create(request_type, json.dumps(request_args),status_codes[request_type][101], "in_progress")
            resp = Response(json.dumps(response_data), status = 200, mimetype = 'application/json' )
            if response_data["success"]:
                data = {
                    "ROOT_URL": db_manager_url,
                    "API_URLS": api_urls,
                    "REQUEST_ID": response_data["requestId"],
                    "REQUEST_TYPE": request_type,
                    "FUNCTION_ID": request_args["functionId"]
                }
                resp = dbmanager.function_delete(data["FUNCTION_ID"])
                # host_config = docker_client.create_host_config(privileged = False, network_mode = 'host')
                # current_container = docker_client.create_container(image = docker_image_name  , name = docker_container_name , environment = data , host_config = host_config)
                # docker_client.start(current_container)
        else:
            resp = custom_util.build_response_for_missing_params(request_types[request_type], required_arg_keys)
    except Exception as e:
        resp = traceback.format_exc()
    return resp

#API endpoints for debugging
@app.route("/containers/list")
def containers():
    try:
        containerz = docker_client.containers()
        resp = custom_util.custom_print(containerz, "<br>")
    except Exception as e:
        resp = traceback.format_exc()
    return resp


@app.route('/containers/logs/<string:container_id>', methods=['GET'])
def container_logs(container_id):
    try:
        resp = docker_client.logs(container_id).replace("\n", "<br>")
    except Exception as e:
        resp = traceback.format_exc()
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
