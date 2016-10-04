import json
import requests
data = {'temperature':'24.3'}
data_json = json.dumps(data)
payload = {'json_payload': data_json, 'apikey': 'YOUR_API_KEY_HERE'}
r = requests.get('http://myserver/emoncms2/api/post', data=payload)