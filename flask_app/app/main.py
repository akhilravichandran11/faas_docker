from flask import Flask, request, jsonify , json , Response
import docker
import requests
import json
import traceback
import random
import datetime
import os


import custom_util
from custom_util import build_response_for_missing_params,build_dict_with_base_data,build_dict_with_request_data,check_dict_for_mandatory_keys
from db_manager_handler import Dbmanager , dbm_api_urls
from constants import request_types,status_codes,container_image_names,service_image_names
from docker_util import Dockerutil

app = Flask(__name__)

#Global Variables based on evn variable MODE
mode = os.environ.get('MODE')
if mode is not None:
    #  URLS for talking to docker containers
    db_manager_url = "http://192.168.1.9:8080"
    faas_manager_url = "http://192.168.1.9:80"
    db_manager_link_url = "http://dbmanager:8080"
    # db_manager_url = "http://" + socket.gethostbyname(socket.gethostname()) + ":8080"
    dbmanager = Dbmanager(db_manager_link_url)
    if mode == "PROD_SWARM":
        swarm = True
        image_names = service_image_names
    else:
        swarm = False
        image_names = container_image_names
else:
    swarm = False
    image_names = container_image_names
    #  URLS for talking to docker containers
    db_manager_url = "http://0.0.0.0:8080"
    faas_manager_url = "http://0.0.0.0:80"
    # db_manager_link_url = "http://dbmanager:8080"
    # db_manager_url = "http://" + socket.gethostbyname(socket.gethostname()) + ":8080"
    dbmanager = Dbmanager(db_manager_url)

faas_api_urls = {
    "service": {
        "remove": "/services/remove"
    }
}

#  Objects Initiated for lifecycle of flask app
docker_client = docker.Client(base_url='unix://var/run/docker.sock')
if mode is not None:

docker_util = Dockerutil(docker_client)
dt_now = datetime.datetime.now()
dict_base_data = build_dict_with_base_data(swarm,db_manager_url, dbm_api_urls,faas_manager_url,faas_api_urls,status_codes)




@app.route("/")
def hello():
    welcome = "Welcome To Madhatterz - FAAS"
    env_mode = "ENV_MODE = "+str(mode)
    swarm_val = "Swarm = " + str(swarm)
    resp = ("\n").join([welcome,env_mode,swarm_val])
    return resp


@app.route("/request/check_status", methods = ['GET'] )
def request_check_status():
    request_type = 'request_status'
    required_arg_keys = ["requestId"]
    try:
        request_args = request.args.to_dict(flat = True)
        if check_dict_for_mandatory_keys(request_args, required_arg_keys):
            resp = dbmanager.request_check_status(request_args["requestId"])
        else:
            resp = build_response_for_missing_params(request_types[request_type], required_arg_keys)
    except Exception as e:
        resp = traceback.format_exc()
    return resp


@app.route("/user/create", methods = ['POST'] )
def user_create():
    request_type = 'create_user'
    required_arg_keys = ["userName", "password"]
    docker_image_name = image_names[request_type]
    docker_cont_or_serv_name = docker_util.gen_random_cont_or_serv_name(swarm,docker_image_name,dt_now)
    try:
        request_args = request.args.to_dict(flat = True)
        if check_dict_for_mandatory_keys(request_args, required_arg_keys):
            response_data = dbmanager.request_create(request_type, json.dumps(request_args), status_codes[request_type][101] + docker_cont_or_serv_name, "in_progress")
            resp = Response(json.dumps(response_data), status = 200, mimetype = 'application/json' )
            if response_data["success"]:
                data = {
                    "USER_NAME" : request_args["userName"],
                    "PASSWORD": request_args["password"]
                }
                data.update(dict_base_data)
                data.update(build_dict_with_request_data(docker_cont_or_serv_name, request_type, response_data["requestId"]))
                docker_util.run_container_or_service(swarm,docker_image_name, docker_cont_or_serv_name, data)
                # resp = dbmanager.user_create(data["USER_NAME"], data["PASSWORD"])
            else:
                resp = build_response_for_missing_params(request_types[request_type],required_arg_keys)
    except Exception as e:
        resp = traceback.format_exc()
    return resp

@app.route("/user/update", methods = ['PUT'] )
def user_update():
    request_type = 'update_user'
    required_arg_keys = ["userId","userName", "password"]
    docker_image_name = image_names[request_type]
    docker_cont_or_serv_name = docker_util.gen_random_cont_or_serv_name(swarm,docker_image_name,dt_now)
    try:
        request_args = request.args.to_dict(flat = True)
        if check_dict_for_mandatory_keys(request_args, required_arg_keys):
            response_data = dbmanager.request_create(request_type, json.dumps(request_args), status_codes[request_type][101] + docker_cont_or_serv_name, "in_progress")
            resp = Response(json.dumps(response_data), status = 200, mimetype = 'application/json' )
            if response_data["success"]:
                data = {
                    "USER_ID": request_args["userId"],
                    "USER_NAME" : request_args["userName"],
                    "PASSWORD": request_args["password"]
                }
                data.update(dict_base_data)
                data.update(build_dict_with_request_data(docker_cont_or_serv_name, request_type, response_data["requestId"]))
                # resp = dbmanager.user_update(data["USER_ID"],data["USER_NAME"],data["PASSWORD"])
                host_config = docker_client.create_host_config(privileged = False, network_mode = 'host')
                current_container = docker_client.create_container(image = docker_image_name  , name = docker_cont_or_serv_name , environment = data , host_config = host_config)
                docker_client.start(current_container)
            else:
                resp = build_response_for_missing_params(request_types[request_type],required_arg_keys)
    except Exception as e:
        resp = traceback.format_exc()
    return resp

@app.route("/user/delete" , methods = ['DELETE'] )
def user_delete():
    request_type = 'delete_user'
    required_arg_keys = ["userName","password","userId"]
    docker_image_name = image_names[request_type]
    docker_cont_or_serv_name = docker_image_name + dt_now.strftime('_cont_%m.%d.%Y_') + str(random.randint(0, 9999))
    try:
        request_args = request.args.to_dict(flat = True)
        if check_dict_for_mandatory_keys(request_args,required_arg_keys):
            response_data = dbmanager.request_create(request_type, json.dumps(request_args),status_codes[request_type][101] + docker_cont_or_serv_name, "in_progress")
            resp = Response(json.dumps(response_data), status = 200, mimetype = 'application/json' )
            if response_data["success"]:
                data = {
                    "USER_ID": request_args["userId"]
                }
                data.update(dict_base_data)
                data.update(build_dict_with_request_data(docker_cont_or_serv_name, request_type, response_data["requestId"]))
                # resp = dbmanager.user_delete(data["USER_ID"])
                host_config = docker_client.create_host_config(privileged = False, network_mode = 'host')
                current_container = docker_client.create_container(image = docker_image_name  , name = docker_cont_or_serv_name , environment = data , host_config = host_config)
                docker_client.start(current_container)
        else:
            resp = build_response_for_missing_params(request_types[request_type], required_arg_keys)
    except Exception as e:
        resp = traceback.format_exc()
    return resp


@app.route("/function/create" , methods = ['POST'] )
def function_create():
    request_type = 'create_function'
    required_arg_keys = ["userId", "userName","password","functionName"]
    docker_image_name = image_names[request_type]
    docker_cont_or_serv_name = docker_image_name + dt_now.strftime('_cont_%m.%d.%Y_') + str(random.randint(0, 9999))
    try:
        request_args = request.args.to_dict(flat = True)
        if check_dict_for_mandatory_keys(request_args,required_arg_keys):
            response_data = dbmanager.request_create(request_type, json.dumps(request_args),status_codes[request_type][101] + docker_cont_or_serv_name, "in_progress")
            resp = Response(json.dumps(response_data), status = 200, mimetype = 'application/json' )
            if response_data["success"]:
                data = {
                    "USER_ID" : request_args["userId"],
                    "USER_NAME": request_args["userName"],
                    "FUNCTION_NAME" : request_args["functionName"],
                    "FUNCTION_CONTENT" : request.data
                }
                data.update(dict_base_data)
                data.update(build_dict_with_request_data(docker_cont_or_serv_name, request_type, response_data["requestId"]))
                # resp = dbmanager.function_create(data["FUNCTION_NAME"],data["FUNCTION_CONTENT"],data["USER_ID"],data["USER_NAME"])
                host_config = docker_client.create_host_config(privileged = False, network_mode = 'host')
                current_container = docker_client.create_container(image = docker_image_name  , name = docker_cont_or_serv_name , environment = data , host_config = host_config)
                docker_client.start(current_container)
        else:
            resp = build_response_for_missing_params(request_types[request_type], required_arg_keys)
    except Exception as e:
        resp = traceback.format_exc()
    return resp

@app.route("/function/update" , methods = ['PUT'] )
def function_update():
    request_type = 'update_function'
    required_arg_keys = ["userId", "userName","password","functionName","functionId"]
    docker_image_name = image_names[request_type]
    docker_cont_or_serv_name = docker_image_name + dt_now.strftime('_cont_%m.%d.%Y_') + str(random.randint(0, 9999))
    try:
        request_args = request.args.to_dict(flat = True)
        if check_dict_for_mandatory_keys(request_args,required_arg_keys):
            response_data = dbmanager.request_create(request_type, json.dumps(request_args),status_codes[request_type][101] + docker_cont_or_serv_name, "in_progress")
            resp = Response(json.dumps(response_data), status = 200, mimetype = 'application/json' )
            if response_data["success"]:
                data = {
                    "USER_ID" : request_args["userId"],
                    "USER_NAME": request_args["userName"],
                    "FUNCTION_ID": request_args["functionId"],
                    "FUNCTION_NAME" : request_args["functionName"],
                    "FUNCTION_CONTENT" : request.data
                }
                data.update(dict_base_data)
                data.update(build_dict_with_request_data(docker_cont_or_serv_name, request_type, response_data["requestId"]))
                # resp = dbmanager.function_update(data["FUNCTION_ID"],data["FUNCTION_NAME"],data["FUNCTION_CONTENT"],data["USER_ID"],data["USER_NAME"])
                host_config = docker_client.create_host_config(privileged = False, network_mode = 'host')
                current_container = docker_client.create_container(image = docker_image_name  , name = docker_cont_or_serv_name , environment = data , host_config = host_config)
                docker_client.start(current_container)
        else:
            resp = build_response_for_missing_params(request_types[request_type], required_arg_keys)
    except Exception as e:
        resp = traceback.format_exc()
    return resp

@app.route("/function/delete" , methods = ['DELETE'] )
def function_delete():
    request_type = 'delete_function'
    required_arg_keys = ["userName","password","functionId"]
    docker_image_name = image_names[request_type]
    docker_cont_or_serv_name = docker_image_name + dt_now.strftime('_cont_%m.%d.%Y_') + str(random.randint(0, 9999))
    try:
        request_args = request.args.to_dict(flat = True)
        if check_dict_for_mandatory_keys(request_args,required_arg_keys):
            response_data = dbmanager.request_create(request_type, json.dumps(request_args),status_codes[request_type][101] + docker_cont_or_serv_name, "in_progress")
            resp = Response(json.dumps(response_data), status = 200, mimetype = 'application/json' )
            if response_data["success"]:
                data = {
                    "FUNCTION_ID": request_args["functionId"]
                }
                data.update(dict_base_data)
                data.update(build_dict_with_request_data(docker_cont_or_serv_name, request_type, response_data["requestId"]))
                # resp = dbmanager.function_delete(data["FUNCTION_ID"])
                host_config = docker_client.create_host_config(privileged = False, network_mode = 'host')
                current_container = docker_client.create_container(image = docker_image_name  , name = docker_cont_or_serv_name , environment = data , host_config = host_config)
                docker_client.start(current_container)
        else:
            resp = build_response_for_missing_params(request_types[request_type], required_arg_keys)
    except Exception as e:
        resp = traceback.format_exc()
    return resp


@app.route("/services/remove<string:service_id>" , methods = ['DELETE'])
def docker_service_remove(service_id):
    request_type = 'docker_service_remove'
    required_arg_keys = ["service_id"]
    try:
        docker_util.remove_service(service_id)
        resp = ""
    except Exception as e:
        resp = traceback.format_exc()
    return resp

#API endpoints for debugging
@app.route("/containers/list")
def docker_containers():
    try:
        containerz = docker_client.containers()
        resp = custom_util.custom_print(containerz, "<br>")
    except Exception as e:
        resp = traceback.format_exc()
    return resp


@app.route('/containers/logs/<string:container_id>', methods=['GET'])
def docker_container_logs(container_id):
    try:
        resp = docker_client.logs(container_id).replace("\n", "<br>")
    except Exception as e:
        resp = traceback.format_exc()
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
