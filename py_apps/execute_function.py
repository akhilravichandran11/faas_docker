import sys
import os
import requests


##################################################
#updating API for request parameters to DB Service
##################################################
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

######################################################
#requesting API for request parameters from DB Service
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

        if response_req['type'] is 'create_function'
                #print request NOK
                return -1
        else
                #get user info
                return resp.json()
                #post_user_db(get_request_api_arg, db_ip_ddress_arg, parameter_arg)

##########################################################
#requesting API to save tehfunction and its contents to DB
##########################################################
def post_function_create_db(db_ip_ddress_arg, userid_json_arg,  **parameter_arg)
	#generating API for getting Function Created
	get_request_api = 'http://' + db_ip_ddress_arg + '/function/'
	 resp = requests.post(get_request_api,json={
        'name': parameter_arg.get("name"),
	'content': parameter_arg.get("content"),
	'userid': userid_json_arg,
        })
        if resp.status_code != 200:
                # This means something went wrong.
                print('GET /request/ {}'.format(resp.status_code))
		return -1
        else:
		print('GET /request/ {}'.format(resp.status_code))
		return 0

##########################################################
#requesting API to get user datad from DB Service
##########################################################
def get_user_db(db_ip_ddress_arg, userid_arg)
        #generating GET API for getting Request from DB Service
        get_request_api = 'http://' + db_ip_ddress_arg + '/user/' + userid_arg
        resp = requests.get(get_request_api)
        if resp.status_code != 200:
                # This means something went wrong.
                print('GET /user/ {}'.format(resp.status_code))
                return -1
        else
                #get user info
                return resp.json()
                #post_user_db(get_request_api_arg, db_ip_ddress_arg, parameter_arg)



##########################################################
#Creation and compilation of the function
##########################################################
def create_function(resp_req_params_arg)
	str = " "
	if len(resp_req_params_arg) > 1:
		for value in range(2,len(resp_req_params_arg)):
			str = str + resp_req_params_arg[value] + " "
	#Dump this code in file
	fobj  = open(temp_file, "w+")
	fobj.write(resp_req_params_arg[1])
	fobj.close

	#exec this file and check output - malkiyat - set return code = 1, failure, 0 for success.
	
	return return_code


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
	user_id_get = resp_req_params[0]
	#Getting user on server - updating request tuple status
        ret_user_get = get_user_db(db_ip_ddress, user_id_get)
        if ret_user_post is -1:
                #user not created properly - updating request tuple status
                put_request_db(request_id, db_ip_ddress, 'RequestFailed')
                return 1
        else:
	resp_req_params.pop(0)
	#Create function contained in resp_req_params
	cre_func_ret = create_function(resp_req_params)	
	if cre_func_ret == -1:
		put_request_db(request_id, db_ip_ddress, 'RequestFailed')
		return 1
	else:
		ret_post_func = post_function_create_db(db_ip_ddress, ret_user_get, name = resp_req_params[1], content = json.dumps(resp_req_params))
		if ret_post_func == -1:
			put_request_db(request_id, db_ip_ddress, 'RequestFailed')
			return 1
		else:
			put_request_db(request_id, db_ip_ddress, 'RequestOK')
			return 0












