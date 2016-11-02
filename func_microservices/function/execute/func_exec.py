import sys
import StringIO
import contextlib
import traceback

code_test_1 = """
def madhat_func(input_data,output_data):
		print str(output_data['out_1'])
"""

main_code = """
print "dude 0"
madhat_func(input_data,output_data)
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
			run_details = ( "Run was Succesfull" if(success) else "Run had Exceptions" )
			return_data = dict(
				requestStatus = run_details,
				result = output_text,
				outputData = dict_output["output_data"]
				)
	return return_data