#!/usr/bin/python
from docker import Client
import custom_util
client = Client(base_url='unix://var/run/docker.sock')

containerz = client.containers()
#containerz = [ {1:"a","c":"d"},{2:"z","x":"y"}]

#print custom_util.custom_print(containerz)
try :
	print client.inspect_container("cc_flak")
except Exception as e:
	print e.message
#print client.logs("cc_flaskapp_cont1")

