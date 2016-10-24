#!/usr/bin/python
from docker import Client
import datetime

docker_client = Client(base_url='unix://var/run/docker.sock')

docker_image_name = 'cc_test_print'
dt_now = datetime.datetime.now()
docker_container_name = docker_image_name + dt_now.strftime('_cont_%m.%d.%Y_')

for i in range(1,5):
  current_container = docker_client.create_container(image = docker_image_name  , name = (docker_container_name + str(i)))
  docker_client.start(current_container)
#  
#for i in range(1,5):
#  current_container = docker_client.remove_container((docker_container_name + str(i)))