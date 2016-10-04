import sys
import os
import requests
import json


######################################################
#requesting API for request object from DB Service
######################################################
def get_request_db(request_id_arg, db_ip_ddress_arg)
        #generating GET API for getting Request from DB Service
        get_request_api = 'http://' + db_ip_ddress_arg + '/request/' + request_id_arg
        resp = requests.get(get_request_api)
        if resp.status_code != 200:
                # This means something went wrong.
                print('GET /request/ {}'.format(resp.status_code))
                #put_request_db(request_id_arg, db_ip_ddress_arg, 'CreationFailed')
       	response_req = json.load(resp.json())
	
	if response_req['type'] is 'create_user'
		#print request NOK
		return -1
	else
		#get user info
		return resp.json() 
		#post_user_db(get_request_api_arg, db_ip_ddress_arg, parameter_arg)

##########################################################
#requesting API for send create user request to DB Service
##########################################################
def post_user_db(request_id_arg, db_ip_ddress_arg, **parameter_arg)
	get_request_api = 'http://' + db_ip_ddress_arg + '/user/'
	 
	resp = requests.post(get_request_api,json={
        'name': parameter_arg.get("name"),
        'password': parameter_arg.get("password"),
        })
        if resp.status_code != 200:
                # This means something went wrong.
                print('POST /user/ {}'.format(resp.status_code))
		return -1
	else
		return 0

##########################################################
#requesting API for updating request object to DB Service
##########################################################
def put_request_db(request_id_arg, db_ip_ddress_arg, set_status_arg)
         #generating GET API for getting Request from DB Service
        get_request_api = 'http://' + db_ip_ddress_arg + '/request/' + request_id_arg
        resp = requests.put(get_request_api, json={'status': set_status_arg})
        if resp.status_code != 200:
                # This means something went wrong.
                print('PUT /request/{} {}'.format(set_status_arg, resp.status_code))
                return -1
        else:
                print('PUT /request/{} {}'.format(set_status_arg, resp.status_code))
                return 0

##########################################################
#Main Program
##########################################################

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

request_id = sys.argv[1]
db_ip_ddress = sys.argv[2]

print("Starting program Function Create for Request ID:" + request_id)
print("DB IP received is " + db_ip_ddress)

print('Fetching Request Object from table')
ret_req_get = get_request_db(request_id, db_ip_ddress)
if ret_req_get is -1:
	#request not received properly - updating request tuple status
	put_request_db(request_id, db_ip_ddress, 'RequestFailed')
	return 1
else:
	resp_req = json.load(ret_req_get)
	resp_req_params = resp_req['parameter'].split(" ")
	
	#Adding user on server - updating request tuple status
	ret_user_post = post_user_db(request_id, db_ip_ddress, name = resp_req_params[0], password = resp_req_params[1])
	if ret_user_post is -1:
		#user not created properly - updating request tuple status
		put_request_db(request_id, db_ip_ddress, 'RequestFailed')
		return 1
	else:
		#user creation Successful - updating request tuple status
		put_request_db(request_id, db_ip_ddress, 'RequestOK')
		return 0
















