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


@app.route("/request/check_status/<string:request_id>", methods = ['GET'] )
def request_check_status(request_id):
    try:
        resp = dbmanager.request_check_status(request_id)
    except Exception as e:
        resp = str(e)
    return resp


@app.route("/user/create", methods = ['POST'] )
def user_create():
    request_type = 'create_user'
    docker_image_name = 'cc_user_create'
    docker_container_name = docker_image_name + dt_now.strftime('_cont_%m.%d.%Y_') + str(random.randint(0,9999))
    try:
        req_json = request.json
        resp_data = dbmanager.request_create(request_type, request.json, status_codes[request_type][101], "in_progress")
        resp = Response(json.dumps(resp_data), status = 200, mimetype = 'application/json' )
        if resp_data["success"]:
            data = {
                "ROOT_URL" : db_manager_url,
                "API_URLS" : api_urls,
                "REQUEST_ID" : resp_data["requestId"],
                "REQUEST_TYPE" : request_type,
                "USERNAME" : req_json["userName"],
                "PASSWORD": req_json["password"]
            }
            host_config = docker_client.create_host_config(privileged = False, network_mode = 'host')
            current_container = docker_client.create_container(image = docker_image_name  , name = docker_container_name , environment = data , host_config = host_config)
            docker_client.start(current_container)
            # while(docker_client.inspect_container(docker_container_name).get('State', dict()).get('Running')):
            #     print ""
            # resp = "Container Name - " + docker_container_name + " \n Logs - " + docker_client.logs( docker_container_name, stdout = True, stderr = True, stream = False, timestamps = False)
    except Exception as e:
        resp = traceback.format_exc()
    return resp


# @app.route("/containers/list")
# def containers():
#     try:
#         containerz = docker_client.containers()
#         resp = custom_util.custom_print(containerz, "<br>")
#     except Exception as e:
#         resp = str(e)
#     return resp
#
#
# @app.route('/containers/logs/<string:container_id>', methods=['GET'])
# def container_logs(container_id):
#     try:
#         resp = docker_client.logs(container_id).replace("\n", "<br>")
#     except Exception as e:
#         resp = str(e)
#     return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
