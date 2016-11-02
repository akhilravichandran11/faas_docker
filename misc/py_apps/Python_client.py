import sys
import os
import requests

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
	post_create_fn_api = 'http://' + db_ip_ddress_arg + 'function/create?userId=' + userid_arg + '&userName=' + username_arg + '&password='+ password_arg +'&functionName=' + functionname_arg
        print("API Called: " + post_create_fn_api)
        resp = requests.post(post_create_fn_api, text=functionContent_arg)
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

def put_create_fn_db(db_ip_ddress_arg, username_arg, password_arg, userid_arg, functionname_arg, functionContent_arg):
        put_create_fn_api = 'http://' + db_ip_ddress_arg + 'function/update?userId=' + userid_arg + '&userName=' + username_arg + '&password='+ password_arg +'&functionName=' + functionname_arg
        print("API Called: " + put_create_fn_api)
	resp = requests.put(put_create_fn_api, text=functionContent_arg)
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

#post_user_db(db_ip_ddress)
#get_user_db(db_ip_ddress)

def create_user():
        print("Creating User")
	username = raw_input("Enter the username ")
	password = raw_input("Enter password ")
	request_id_create_user = post_user_db(db_ip_ddress, username, password)
def create_function():
        print("Creating Function ")
	username = raw_input("Enter the username ")
	functionname = raw_input("Enter the function name ")
	functionfile = raw_input("Enter function file name ")
	with open(functionfile, 'r') as content_file:
    		functionContent = content_file.read()
	request_id_create_func = post_create_fn_db(db_ip_ddress, username, password, userid, functionname, functionContent)
def execute_function():
        print("Executing Function")
def create_user_bulk():
        print("Creating User in Bulk")
def create_function_bulk():
        print("Creating Function in bulk")
def execute_function_bulk():
        print("Executing Function in bulk")
def poll():
        print("Polling")

selection = {0 : create_user,
                1 : create_function,
                2 : execute_function,
                3 : create_user_bulk,
                4 : create_function_bulk,
                5 : execute_function_bulk,
                6 : poll,
}

db_ip_ddress = sys.argv[1]

print("IP address of FAAS service is " + db_ip_ddress)
print("Hello User...")
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

menu_option = 0
while menu_option >= 0 and menu_option <= 6:
	print("Please enter your Choice")
	print("0 - Create a User")
	print("1 - Create a Function")
	print("2 - Execute a Function")
	print("3 - Create Users in bulk from file")
	print("4 - Create Functions in bulk for a user")
	print("5 - Execute Functions in bulk for a user ")
	print("6 - Poll on a request ID")
	print("7 - Exit")
	menu_option = input()
	if menu_option >= 0 and menu_option <= 6:
		selection[menu_option]()

