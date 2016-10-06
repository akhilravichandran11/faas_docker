import sys
import os
import requests


##########################################################
#updating API for request parameter - status to DB Service
##########################################################
def put_request_db(request_id_arg, db_ip_ddress_arg, set_status_arg)
	 #generating GET API for getting Request from DB Service
        get_request_api = 'http://' + db_ip_ddress_arg + '/request/' + request_id_arg
	resp = requests.put(get_request_api, json={'status': set_status_arg})
        if resp.status_code != 200:
                # This means something went wrong.
                print('PUT /request/{} {}'.format(request_id_arg, resp.status_code))
                return -1
        else:
                print('PUT /request/{} {}'.format(request_id_arg, resp.status_code))
                return 0


###########################################################
#updating API for request parameters - result to DB Service
###########################################################
def put_request_result_db(request_id_arg, db_ip_ddress_arg, set_result_arg)
         #generating GET API for getting Request from DB Service
        get_request_api = 'http://' + db_ip_ddress_arg + '/request/' + request_id_arg
        resp = requests.put(get_request_api, json={'result': set_result_arg})
        if resp.status_code != 200:
                # This means something went wrong.
                print('PUT /request/{} {}'.format(request_id_arg, resp.status_code))
                return -1
        else:
                print('PUT /request/{} {}'.format(request_id_arg, resp.status_code))
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

        if response_req['type'] is 'execute_function'
                #print request NOK
                return -1
        else
                #get user info
                return resp.json()
                #post_user_db(get_request_api_arg, db_ip_ddress_arg, parameter_arg)

##########################################################
#requesting API to save tehfunction and its contents to DB
##########################################################
def get_function_db(db_ip_ddress_arg, function_id_arg)
	#generating API for getting Function Created
	get_request_api = 'http://' + db_ip_ddress_arg + '/function/' + function_id_arg
	 resp = requests.get(get_request_api)
        if resp.status_code != 200:
                # This means something went wrong.
                print('GET /request/ {}'.format(resp.status_code))
		return -1
        else:
		print('GET /request/ {}'.format(resp.status_code))
		return resp.json()

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
def execute_function(resp_req_params_arg, content)
	str = " "
	if len(resp_req_params_arg) > 2:
		for value in range(2,len(resp_req_params_arg)):
			str = str + resp_req_params_arg[value] + " "
	#Dump this code in file resp_req_params_arg[2]
	fobj  = open(temp_file, "w+")
	fobj.write(content)
	fobj.close

	#exec this file and save output and result - malkiyat - set return code = 1, failure, 0 for success.
	
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
if ret_req_get == -1:
        #request not received properly - updating request tuple status
        put_request_db(request_id, db_ip_ddress, 'RequestFailed')
        return 1
else:
	resp_req = json.load(ret_req_get)
        resp_req_params = resp_req['parameter'].split(" ")
	user_id_get = resp_req_params[0]
	#Getting user on server - updating request tuple status
        ret_user_get = get_user_db(db_ip_ddress, user_id_get)
        if ret_user_post == -1:
                #user not created properly - updating request tuple status
                put_request_db(request_id, db_ip_ddress, 'RequestFailed')
                return 1
        else:
	resp_req_params.pop(0)
	get_func_ret = get_function_db(db_ip_ddress, resp_req_params[1])
	if get_func_ret == -1
		#function not retrieved properly - updating request tuple status
                put_request_db(request_id, db_ip_ddress, 'RequestFailed')
                return 1
	else:
		#Execute function contained in resp_req_params
		get_func_ret_list = json.loads(get_func_ret)
		cre_func_ret = execute_function(resp_req_params, get_func_ret_list['content'])	
		if cre_func_ret == -1:
			put_request_db(request_id, db_ip_ddress, 'RequestFailed')
			return 1
		else:
			func_res_ret = put_request_result_db(request_id, db_ip_ddress, cre_func_ret)
			if func_res_ret == -1:
				put_request_db(request_id, db_ip_ddress, 'RequestFailed')
				return 1
			else:
				put_request_db(request_id, db_ip_ddress, 'RequestOK')
				return 0
	











