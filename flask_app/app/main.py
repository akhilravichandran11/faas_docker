import sys
import os
from flask import Flask
import docker
import logging
import requests
import json

import custom_util

app = Flask(__name__)

docker_client = docker.Client(base_url='unix://var/run/docker.sock')

db_manager_url = "http://dbmanager:8080"

db_manager_url_api = {
    "request":{
    "check_status": "/dbmanager/rest/request/"
    }
}

@app.route("/")
def hello():
    return  "Welcome To Madhatterz - FAAS"


@app.route("/request/check_status/<string:request_id>" , methods = ['GET'] )
def request_check_status(request_id):
    resp = ""
    try:
        request_check_status_url = db_manager_url + db_manager_url_api["request"]["check_status"] + request_id
        # request_obj = requests.get(request_check_status_url)
        request_obj = requests.get('http://dbmanager:8080/dbmanager/rest/request/B8323A57-AA95-4C91-AFE7-60E9A748A4E5')
        resp = str(request_obj.status_code)
        # resp = custom_util.return_request_response(request_obj)
    except Exception as e:
        resp = str(e)
    return resp

@app.route("/containers/list")    
def containers():
    log_result = ""
    try:
        containerz = docker_client.containers()
        log_result = custom_util.custom_print(containerz,"<br>") 
    except Exception as e:
        log_result = str(e)
    return  log_result

@app.route('/containers/logs/<variable>' , methods = ['GET'] )
def container_logs(variable):
    log_result = ""
    try:
        log_result = docker_client.logs(variable).replace("\n","<br>")
    except Exception as e:
        log_result =  str(e)
    return log_result
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True , port=80 )
