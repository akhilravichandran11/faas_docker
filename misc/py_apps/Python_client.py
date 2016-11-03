import sys
import os
import termios
import requests
import threading
import json

request_id_list = []

##################################################
#Users
##################################################
def post_user_db( db_ip_ddress_arg, username_arg, password_arg):
        post_user_api = 'http://' + db_ip_ddress_arg + '/user/create?userName=' + username_arg + '&password=' + password_arg
        print("API Called: " + post_user_api)
	
	resp = requests.post(post_user_api, {})
	print resp
	print(resp.json())
        if resp.status_code != 200:
                print('POST /user/create/ {}'.format(resp.status_code))
                return -1
        else:
                print('POST /user/create/ {}'.format(resp.status_code))
                return resp

def get_user_db(db_ip_ddress_arg, username):
        get_user_api = 'http://' + db_ip_ddress_arg + ':8080/dbmanager/rest/users/' + username
        resp = requests.get(get_user_api)
        print(resp.json())
	print(resp)
        if resp.status_code != 200:
                print('GET /dbmanager/rest/users/ {}'.format(resp.status_code))
                return -1
        else:
                print('GET /dbmanager/rest/users/ {}'.format(resp.status_code))
                return resp

def put_user_db(db_ip_ddress_arg, username_arg, password_arg, userid_arg):
        put_user_api = 'http://' + db_ip_ddress_arg + '/user/update?userId=' + userid_arg + '&userName=' + username_arg + '&password=' + password_arg
        print("API Called: " + put_user_api)
	resp = requests.put(put_user_api,{})
	print(resp.json())
        if resp.status_code != 200:
                print('PUT /user/update/ {}'.format(resp.status_code))
                return -1
        else:
                print('PUT /user/update/ {}'.format(resp.status_code))
                return resp

def del_user_db(db_ip_ddress_arg, username_arg, password_arg, userid_arg):
        del_user_api = 'http://' + db_ip_ddress_arg + '/user/delete?userId=' + userid_arg + '&userName=' + username_arg + '&password=' + password_arg
        print("API Called: " + del_user_api)
	resp = requests.delete(del_user_api)
        print(resp.json())
        if resp.status_code != 200:
                print('DEL /user/delete/ {}'.format(resp.status_code))
                return -1
        else:
                print('DEL /user/delete/ {}'.format(resp.status_code))
                return resp

##################################################
#Functions
##################################################

def post_create_fn_db(db_ip_ddress_arg, username_arg, password_arg, userid_arg, functionname_arg, functionContent_arg):
	post_create_fn_api = 'http://' + db_ip_ddress_arg + '/function/create?userId=' + userid_arg + '&userName=' + username_arg + '&password='+ password_arg +'&functionName=' + functionname_arg
        print("API Called: " + post_create_fn_api)
        resp = requests.post(post_create_fn_api, data=functionContent_arg)
	print(resp)
        print(resp.json())
        if resp.status_code != 200:
                print('POST /function/create/ {}'.format(resp.status_code))
                return -1
        else:
                print('POST /function/create {}'.format(resp.status_code))
                return resp

def get_create_fn_db( db_ip_ddress_arg):
        get_user_api = 'http://' + db_ip_ddress_arg + ':8080/dbmanager/rest/functions/'
        resp = requests.get(get_user_api)
        print(resp.json())
        print(resp)
        if resp.status_code != 200:
                print('GET /request/ {}'.format(resp.status_code))
                return -1
        else:
                print('GET /request/ {}'.format(resp.status_code))
                return 0

def put_update_fn_db(db_ip_ddress_arg, username_arg, password_arg, userid_arg, functionname_arg,  functionid_arg, functionContent_arg):
        put_update_fn_api = 'http://' + db_ip_ddress_arg + '/function/update?userId=' + userid_arg + '&userName=' + username_arg + '&password='+ password_arg + '&functionId=' + functionid_arg + '&functionName=' + functionname_arg
        print("API Called: " + put_update_fn_api)
	resp = requests.put(put_update_fn_api, data=functionContent_arg)
        print(resp.json())
        if resp.status_code != 200:
                print('PUT /function/update {}'.format(resp.status_code))
                return -1
        else:
                print('PUT /function/update {}'.format(resp.status_code))
                return resp

def del_fn_db(db_ip_ddress_arg, username_arg, password_arg, functionid_arg):
        del_fn_api = 'http://' + db_ip_ddress_arg + '/function/delete?userName=' + username_arg + '&password=' + password_arg + '&functionId=' + functionid_arg
        
	print("API Called: " + del_fn_api)
	resp = requests.delete(del_fn_api)
        print(resp.json())
        if resp.status_code != 200:
                print('PUT /function/delete {}'.format(resp.status_code))
                return -1
        else:
                print('PUT /function/delete {}'.format(resp.status_code))
                return resp

def exec_fn_db(db_ip_ddress_arg, username_arg, password_arg, functionid_arg, functionargs_arg):
        exec_fn_api = 'http://' + db_ip_ddress_arg + '/function/execute?userName=' + username_arg + '&password=' + password_arg + '&functionId=' + functionid_arg
        
	print("API Called: " + exec_fn_api)
	resp = requests.post(exec_fn_api, json=functionargs_arg)
	print(resp)
        print(resp.json())
        if resp.status_code != 200:
                print('PUT /function/execute {}'.format(resp.status_code))
                return -1
        else:
                print('PUT /function/execute {}'.format(resp.status_code))
                return resp

##################################################
#RequestID
##################################################
def get_request_db(db_ip_ddress_arg, requestid_arg):
        get_request_api = 'http://' + db_ip_ddress_arg + '/request/check_status?requestId=' + requestid_arg
	print("API Called: " + get_request_api)
        resp = requests.get(get_request_api)
        print(resp)
	print(resp.json())	
        if resp.status_code != 200:
                print('GET /request/check_status/ {}'.format(resp.status_code))
                return -1
        else:
                print('GET /request/check_status/ {}'.format(resp.status_code))
                return resp

#post_user_db(db_ip_ddress)
#get_user_db(db_ip_ddress)

def create_user():
        print("Creating User")
	username = raw_input("Enter the username ")
	password = raw_input("Enter password ")

	request_id_create_user = post_user_db(db_ip_ddress, username, password)
	#print(request_id_create_user.json()["requestId"])
	#print()
	#request_id_list.append(request_id_create_user.json()["requestId"])


def update_user():
        print("Updating User")
	username = raw_input("Enter the username ")
	password = raw_input("Enter password ")
	
	get_user = 'http://' + db_ip_ddress + ':8080/dbmanager/rest/functions/' + username
	resp_db = requests.get(get_user)	
	userid = resp_db.json()['userId']
	
	request_id_update_user = put_user_db(db_ip_ddress, username, password, userid)


def delete_user():
        print("Deleting User")
	username = raw_input("Enter the username ")
	password = raw_input("Enter password ")
	
	get_user = 'http://' + db_ip_ddress + ':8080/dbmanager/rest/functions/' + username
	resp_db = requests.get(get_user)	
	userid = resp_db.json()['userId']
	
	del_user_db(db_ip_ddress, username, password, userid)


def create_function():
        print("Creating Function ")
	username = raw_input("Enter the username ")
	password = raw_input("Enter password ")
	#userid = raw_input("Enter the userID")
	functionname = raw_input("Enter the function name ")
	functionfile = raw_input("Enter function file name ")
	
	get_user = 'http://' + db_ip_ddress + ':8080/dbmanager/rest/users/' + username
	resp_db = requests.get(get_user)	
	userid = resp_db.json()['userId']

	with open(functionfile, 'r') as content_file:
		functionContent = content_file.read()
	print(functionContent)
	request_id_create_func = post_create_fn_db(db_ip_ddress, username, password, userid, functionname, functionContent)

def update_function():
        print("Updating Function ")
	username = raw_input("Enter the username ")
	password = raw_input("Enter password ")
	userid = raw_input("Enter the userID")
	functionname = raw_input("Enter the function name ")
	functionfile = raw_input("Enter function file name ")

	get_user = 'http://' + db_ip_ddress + ':8080/dbmanager/rest/users/' + username
	resp_db = requests.get(get_user)	
	userid = resp_db.json()['userId']

	get_fid = 'http://' + db_ip_ddress + ':8080/dbmanager/rest/functions/' + username + '/' + functionname
	resp_db = requests.get(get_fid)	
	functionid = resp_db.json()['functionId']

	with open(functionfile, 'r') as content_file:
    		functionContent = content_file.read()
	print(functionContent)

	request_id_update_func = put_update_fn_db(db_ip_ddress, username, password, userid, functionname,  functionid, functionContent)


def delete_function():
        print("Deleting Function ")
	username = raw_input("Enter the username ")
	password = raw_input("Enter password ")
	userid = raw_input("Enter the userID")
	functionname = raw_input("Enter the function name ")

	get_fid = 'http://' + db_ip_ddress + ':8080/dbmanager/rest/functions/' + username + '/' + functionname
	resp_db = requests.get(get_fid)	
	functionid = resp_db.json()['functionId']
	print('Function ID: ' + functionid)
	
	request_id_delete_func = del_fn_db(db_ip_ddress, username, password, functionid)


def execute_function():
        print("Executing Function")
	username = raw_input("Enter the username ")
	password = raw_input("Enter password ")
	functionname = raw_input("Enter the function name ")
	functionargs_file = raw_input("Enter the file name containing arguments ")
		
	get_fid = 'http://' + db_ip_ddress + ':8080/dbmanager/rest/functions/' + username + '/' + functionname
	resp_db = requests.get(get_fid)	
	functionid = resp_db.json()['functionId']
	print('Function ID: ' + functionid)
	
	with open(functionargs_file, 'r') as content_file:
    		functionargs = content_file.read()
	print(functionargs)
	request_id_exec_func = exec_fn_db(db_ip_ddress, username, password, functionid, functionargs)

#def post_user_db_th(db_ip_ddress_th, user_name_th, password_th):
	#request_id_create_user = post_user_db(db_ip_ddress_th, user_name_th, password_th)
	#request_id_list.append(request_id_create_user.json()["requestId"])
	#print(request_id_create_user.json()["requestId"])
	#return request_id_create_user
def create_user_bulk():
        print("Creating User in Bulk")
	no_of_users = int(raw_input("Enter the number of users required "))
	prefix = raw_input("Enter a prefix ")
	password = "me"
	
	#threads = []
	for i in range(no_of_users):
		user_name = prefix + '_user_' + str(i)
		print(user_name)
		#t = threading.Thread(target=post_user_db_th, args = (db_ip_ddress, user_name, password))
		#threads.append(t)
		#t.start()
		#request_id_create_user = t.join()
		request_id_create_user = post_user_db(db_ip_ddress, user_name, password)
		#if request_id_create_user.json()["success"] == "True":
		print(request_id_create_user.json()["requestId"])
		request_id_list.append(request_id_create_user.json()["requestId"])


def update_user_bulk():
        print("Creating User in Bulk")


def delete_user_bulk():
	print("Deleting User in Bulk")
	#username = raw_input("Enter the username") 
	prefix = raw_input("Enter a prefix ")
	password = "me"
	
	user_name = prefix + '_user_' + str(i)
	
	get_user = 'http://' + db_ip_ddress + ':8080/dbmanager/rest/users/' + user_name
	resp_db = requests.get(get_user)
	print(resp_db)
	if resp_db.json() != {"errorMessage":"Object with the name does not exist"}:
		userid = resp_db.json()['userId']
	
	while resp_db.json() != {"errorMessage":"Object with the name does not exist"}:
		print(user_name)
		request_id_delete_user = del_user_db(db_ip_ddress, user_name, password, userid)
		request_id_list.append(request_id_delete_user.json()["requestId"])
		i += 1
		print("I: " + str(i))
		user_name = prefix + '_user_' + str(i)
		get_user = 'http://' + db_ip_ddress + ':8080/dbmanager/rest/users/' + user_name
		resp_db = requests.get(get_user)
		if resp_db.json() != {"errorMessage":"Object with the name does not exist"}:
			userid = resp_db.json()['userId']
		print(user_name)
	
	

def create_function_bulk():
        print("Creating Function in bulk")
	no_of_funcs = int(raw_input("Enter the number of functions required "))
	prefix = raw_input("Enter a prefix ")
	username = raw_input("Enter the username ")
	password = raw_input("Enter password ")
	get_user = 'http://' + db_ip_ddress + ':8080/dbmanager/rest/users/' + username
	resp_db = requests.get(get_user)	
	userid = resp_db.json()['userId']
	print('UserID: ' + userid)
	with open("me.py", 'r') as content_file:
    		functionContent = content_file.read()
	print(functionContent)
	for i in range(no_of_funcs):
		func_name = prefix + '_func_' + str(i)
		request_id_create_func = post_create_fn_db(db_ip_ddress, username, password, userid, func_name, functionContent)
		#if request_id_create_user.json()["success"] == "True":
		print(request_id_create_func.json()["requestId"])
		request_id_list.append(request_id_create_func.json()["requestId"])

def update_function_bulk():
        print("Updating Function in bulk")
	no_of_funcs = int(raw_input("Enter the number of functions required "))
	prefix = raw_input("Enter a prefix ")
	username = raw_input("Enter the username ")
	password = raw_input("Enter password ")
	get_user = 'http://' + db_ip_ddress + ':8080/dbmanager/rest/users/' + username
	resp_db = requests.get(get_user)	
	userid = resp_db.json()['userId']
	print('UserID: ' + userid)
	with open("me.py", 'r') as content_file:
    		functionContent = content_file.read()
	print(functionContent)
	#for i in range(no_of_funcs):
		#func_name = prefix + '_func_' + str(i)
		#request_id_create_func = post_create_fn_db(db_ip_ddress, username, password, userid, func_name, functionContent)
		#if request_id_create_user.json()["success"] == "True":
		#print(request_id_create_func.json()["requestId"])
		#request_id_list.append(request_id_create_func.json()["requestId"])
	func_name = prefix + '_func_' + str(i)
	
	get_func = 'http://' + db_ip_ddress + ':8080/dbmanager/rest/users/' + username + '/'+ func_name
	resp_db = requests.get(get_func)
	
	if resp_db.json() != {"errorMessage":"Object with the name does not exist"}:
		functionid = resp_db.json()['functionId']
		
	get_fid = 'http://' + db_ip_ddress + ':8080/dbmanager/rest/functions/' + username + '/' + functionname
	resp_db = requests.get(get_fid)	
	functionid = resp_db.json()['functionId']
	print('Function ID: ' + functionid)
	
	with open(functionargs_file, 'r') as content_file:
    		functionargs = content_file.read()
	print(functionargs)
	
	while resp_db.json() != {"errorMessage":"Object with the name does not exist"}:
		request_id_update_func = put_update_fn_db(db_ip_ddress, username, password, userid, func_name,  functionid, functionContent)
		request_id_list.append(request_id_create_func.json()["requestId"])
		i += 1
		func_name = prefix + '_func_' + str(i)
		get_func = 'http://' + db_ip_ddress + ':8080/dbmanager/rest/users/' + username + '/'+ func_name
		resp_db = requests.get(get_func)
		if resp_db.json() != {"errorMessage":"Object with the name does not exist"}:
			functionid = resp_db.json()['functionId']
def delete_function_bulk():
        print("Deleting Function in bulk")


def execute_function_bulk():
        print("Executing Function in bulk")
	username = raw_input("Enter the username ")
	password = raw_input("Enter password ")
	no_of_funcs = int(raw_input("Enter the number of functions to be executed "))
	functionname = raw_input("Enter the function name ")
	functionargs_file = raw_input("Enter the file name containing arguments ")

	get_func = 'http://' + db_ip_ddress + ':8080/dbmanager/rest/functions/' + username + '/' + functionname
	resp_db = requests.get(get_func)	
	functionid = resp_db.json()['functionId']
	
	print('FunctionID: ' + functionid)
	
	input_dict = {}
	output_dict = {}
	function_arg_dict = {}
	
	
	for i in range(no_of_funcs):
			
		input_dict = {}
		output_dict = {}
		function_arg_dict = {}

		data = {
			"input_data": {
			"val_1" : i,
			"val_2": (10- i)
			},
			"output_data": {
			"fib_val_1" : "MadHat_Out_1",
			"fib_val_2" : "MadHat_Out_2"
			}
		}
		#input_dict["val_2"] = 10 - i
		#output_dict["fib_val_1"] = "MadHat_Out_1"
		#output_dict["fib_val_2"] = "MadHat_Out_2"
		#function_arg_dict ["input_data"] = input_dict
		#function_arg_dict ["output_data"] = output_dict
		#functionargs = json.dumps(function_arg_dict)

		#print("JSON OBJECT: " + functionargs)

 		request_id_exec_func = exec_fn_db(db_ip_ddress, username, password, functionid, data)
		print(request_id_exec_func.json()["requestId"])
		request_id_list.append(request_id_exec_func.json()["requestId"])
	

def poll():
        print("Polling")
	poll_input = raw_input("Enter Request ID to poll or enter POLLALL to poll all requests ")
	if poll_input == "POLLALL":
		print("polling all requestIDs")
		print(request_id_list)
		for request_inst in request_id_list:
			get_request_db(db_ip_ddress, request_inst)
	else:
		print("pollrequestID")
		get_request_db(db_ip_ddress, poll_input)

selection = {0 : create_user,
                1 : update_user,
		2 : delete_user,
		3 : create_function,
                4 : update_function,
		5 : delete_function,
		6 : execute_function,
                7 : create_user_bulk,
                8 : update_user_bulk,
		9 : delete_user_bulk,
		10 : create_function_bulk,
                11 : update_function_bulk,
		12 : delete_function_bulk,
		13 : execute_function_bulk,
		14 : poll,
}

db_ip_ddress = sys.argv[1]

print("IP address of FAAS service is " + db_ip_ddress)
print("Hello User...")
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

menu_option = 0
while menu_option >= 0 and menu_option <= 14:
	print("Please enter your Choice")
	print("0 - Create a User")
	print("1 - Update a User")
	print("2 - Delete a User")
	print("3 - Create a Function")
	print("4 - Update a Function")
	print("5 - Delete a Function")
	print("6 - Execute a Function")
	print("7 - Create Users in bulk")
	print("8 - Update Users in bulk")
	print("9 - Delete Users in bulk")
	print("10 - Create Functions in bulk for a user")
	print("11 - Update Functions in bulk for a user")
	print("12 - Delete Functions in bulk for a user")
	print("13 - Execute Functions in bulk for a user ")
	print("14 - Poll on a request ID")
	print("15 - Exit")
	termios.tcflush(sys.stdin, termios.TCIOFLUSH)
	menu_option = int(input())
	print(menu_option)
	if menu_option >= 0 and menu_option <= 14:
		selection[menu_option]()
	
