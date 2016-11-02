#!/usr/bin/python


import sys
import StringIO
import contextlib
import traceback

function_input =  {
	"i" : 1,
	"j" : 200,
	"val" : 500
}

function_output = {
	"out_1" : "Dude WTF 1",
	"out_2" : "Dude WTF 2"
}


code_test_1 = """
def fib_iterative(n):
	i = 0
	j = 1
	k = 0
	while(n>0):
		k = i + j
		i = j
		j = k
		n = n -1
	return k
global fib_iterative
def madhat_func(input_data,output_data):
	i = [0,1]
	val = input_data["val"]
	for j in i :
		val = val+ j
		print "Inside Madhat " + str(val)
	output_data["val"]=val
	output_data["val_fib_non_iter_1"]=fib_iterative(7)
"""
main_code = """
madhat_func(input_data,output_data)
"""

main_code_1 = """
print "dude 0"
print "dude type 1" + str(type(input_data))
print str(input_data['val'])
print "dude 2"
"""

@contextlib.contextmanager
def stdoutIO(stdout=None):
	old = sys.stdout
	if stdout is None:
		stdout = StringIO.StringIO()
	sys.stdout = stdout
	try:
		yield stdout
	finally:
		sys.stdout = old


def execute_function(function_content, function_output, function_input):
	function_content = code_test_1
	# exec_code = function_content + main_code
	exec_code = main_code_1
	dict_output = {"output_data": function_output}
	dict_input = {"input_data": function_input}
	success = True
	try:
		print "Before - Output Data = " + str(dict_output["output_data"])
		with stdoutIO() as s:
			print "Started Context Manager"
			exec (exec_code, dict_output, dict_input)
			print "Ended Context Manager"
		print "After - Output Data = " + str(dict_output["output_data"])
		print "Start Output :\n"
		output_text = s.getvalue()
		print output_text
		print "End Output \n"
	except Exception as e:
		success = False
		print "Entered Exception :\n"
		output_text = traceback.format_exc()
		print output_text
		print "Completed Exception \n"
	finally:
		if success:
			return_data = dict(
				run_success=str(success),
				output_text=output_text,
				output_data=dict_output["output_data"]
			)
		else:
			return_data = dict(
				run_success=str(success),
				exception_text=output_text,
				output_data=dict_output["output_data"]
			)
	return return_data
	
execute_function(code_test_1, function_output, function_input)
