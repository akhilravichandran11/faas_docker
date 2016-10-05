import sys
import os
import requests
import json


print "Dude 1"
r = requests.get('http://192.168.1.9:8080/dbmanager/rest/request/B8323A57-AA95-4C91-AFE7-60E9A748A4E5')
print r.status_code
print r.text
print "Dude 2"