#!/usr/bin/python

import docker
import random
import uuid
import re
class Dockerutil:
    def __init__(self, docker_client):
        self.docker_client = docker_client

    def gen_random_cont_or_serv_name(self,swarm,cont_or_serv_name,datetime_now):
        if swarm:
            docker_cont_or_serv_name = cont_or_serv_name + "_" + str(uuid.uuid4().hex)
        else:
            docker_cont_or_serv_name = cont_or_serv_name + datetime_now.strftime('_cont_%m.%d.%Y_') + str(random.randint(0, 9999))
        return docker_cont_or_serv_name


    def get_docker_logs_after_exit(self,docker_container_name):
        while(self.docker_client.inspect_container(docker_container_name).get('State', dict()).get('Running')):
            print ""
        resp = "Container Name - " + docker_container_name + " \n Logs - " + self.docker_client.logs( docker_container_name, stdout = True, stderr = True, stream = False, timestamps = False)
        return resp

    def run_container_or_service(self,swarm,docker_image_name,docker_cont_or_serv_name,data):
        if swarm:
            self.run_service(docker_image_name, docker_cont_or_serv_name, data)
        else:
            self.run_container_with_host_config(docker_image_name, docker_cont_or_serv_name, data)

    def run_container_with_host_config(self,docker_image_name,docker_cont_or_serv_name,data):
        host_config = self.docker_client.create_host_config(privileged = False, network_mode = 'host')
        current_container = self.docker_client.create_container(image = docker_image_name, name = docker_cont_or_serv_name, environment = data, host_config = host_config)
        self.docker_client.start(current_container)

    def run_service(self,docker_image_name,docker_cont_or_serv_name,data):
        # docker_client_1 = docker.Client(base_url='unix://var/run/docker.sock')
        container_spec = docker.types.ContainerSpec(image = "192.168.1.9:5000/cc_user_create", env = ["SWARM=SWARM"])
        task_tmpl = docker.types.TaskTemplate(container_spec)
        service_id = self.docker_client.create_service(task_tmpl, name="cc_sw_user_create_1")

    def remove_service(self,docker_service_name):
        self.docker_client.remove_service(docker_service_name)
