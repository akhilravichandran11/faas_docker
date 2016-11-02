import sys
import StringIO
import contextlib
import traceback

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

def compile_function(function_content):
	success = True
	output_text = ""
	exec_code = function_content
	success = True
	try:
		with stdoutIO() as s:
			compile(exec_code,"test_code","exec")
		output_text = s.getvalue()
	except Exception as e:
		success = False
		output_text = traceback.format_exc()
	finally:
			run_details = ( "Function Compiled Succesfully" if(success) else "Compilation Exceptions" )
			return_data = dict(
			  success = success,
				requestStatus = run_details,
				result = output_text
				)
	return return_data