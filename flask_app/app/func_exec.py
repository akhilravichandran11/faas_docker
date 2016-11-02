import sys
import StringIO
import contextlib
import traceback

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
	exec_code = function_content + main_code
	dict_output = {"output_data": function_output}
	dict_input = {"input_data": function_input}
	success = True
	try:
		with stdoutIO() as s:
			exec (exec_code, dict_output, dict_input)
		output_text = s.getvalue()
	except Exception as e:
		success = False
		output_text = traceback.format_exc()
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