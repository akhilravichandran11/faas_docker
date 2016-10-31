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
	yield stdout
	sys.stdout = old

code = """
def madhat_func(data):
	i = [0,1]
	for j in i :
		print data["dude"]
"""
main_code = """
resp = ""
try:
	resp = madhat_func(data)
except Exception as e:
	resp = traceback.format_exc()
	print resp

"""
main_code_2 = """
resp = madhat_func(data)
"""
data = {
	"dude" : "dude"
}
resp = ""
try:
	with stdoutIO() as s:
		exec(code+main_code_2,{"data":data})
	resp = "out:" + s.getvalue()
except Exception as e:
	resp = traceback.format_exc()
	resp = "exp:" + resp
print resp