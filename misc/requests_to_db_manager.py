import sys
import os
import requests
import json

data = {'temperature':'24.3'}
data_json = json.dumps(data)
payload = {'json_payload': data_json, 'apikey': 'YOUR_API_KEY_HERE'}
r = requests.get('http://192.168.1.9:8080/dbmanager/rest/users')

print r.status_code
print r.json()
print r.text
print r.headers['content-type']