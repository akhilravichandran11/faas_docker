import sys
import os
import requests
import json


print "Dude 1"
r = requests.get('http://192.168.1.9:8080/dbmanager/rest/request/B8323A57-AA95-4C91-AFE7-60E9A748A4E5')
print r.status_code
print r.text
print "Dude 2"
# data = {
#   "requestId": None,
#   "requestType":"Create User",
#   "requestStatus":"Starting",
#   "requestParameters": None,
#   "result":"Still calculating",
#   "requestor":{"password":"qwerty123","userName":"abc","userId": None}
# }
# data_json = json.dumps(data)
# headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
# r = requests.post('http://192.168.1.9:8080/dbmanager/rest/request' , data = data_json , headers = headers)

# print r.status_code
# # print r.json()
# print r.text
# print r.headers['content-type']