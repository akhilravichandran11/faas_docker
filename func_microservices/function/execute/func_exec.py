import sys
import StringIO
import contextlib
import traceback

main_code_post = """
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
	# print "function_content = " + function_content
	# print "function_output = " + str(function_output)
	# print "function_input = " + str(function_input)
	exec_code = function_content + main_code_post
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
				result = str(dict(
					output_text = output_text,
					outputData = str(dict_output["output_data"] )
					)),
				outputData = str(dict_output["output_data"])
			)
	return return_data