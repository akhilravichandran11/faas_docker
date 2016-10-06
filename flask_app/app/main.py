import sys
import os
from flask import Flask
import docker
import logging
import requests
import json

import custom_util
import db_manager_handler

app = Flask(__name__)


#  URLS for talking to docker containers
db_manager_url = "http://dbmanager:8080"


#  Objects Initiated for lifecycle of flask app
docker_client = docker.Client(base_url='unix://var/run/docker.sock')
dbmanager = Dbmanager(db_manager_url)


@app.route("/")
def hello():
    return  "Welcome To Madhatterz - FAAS"


@app.route("/request/check_status/<string:request_id>" , methods = ['GET'] )
def request_check_status(request_id):
    resp = ""
    try:
        resp = dbmanager.request_check_status(request_id)
    except Exception as e:
        resp = str(e)
    return resp

@app.route("/user/create" , methods = ['POST'])
def user_create(): 

@app.route("/containers/list")    
def containers():
    log_result = ""
    try:
        containerz = docker_client.containers()
        log_result = custom_util.custom_print(containerz,"<br>") 
    except Exception as e:
        log_result = str(e)
    return  log_result

@app.route('/containers/logs/<string:container_id>' , methods = ['GET'] )
def container_logs(container_id):
    log_result = ""
    try:
        log_result = docker_client.logs(container_id).replace("\n","<br>")
    except Exception as e:
        log_result =  str(e)
    return log_result
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True , port=80 )
