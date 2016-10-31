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
	i = [0,1
	for j in i :
		data["dude"] = data["dude"]+ j
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
	"dude" : 2
}
resp = ""
temp = sys.stderr
try:
	print "data 1 = "+ str(data)
	with stdoutIO() as s:
		print "dude 3"
		exec(code+main_code_2,{"data":data})
	print "data 2 = "+ str(data)
	resp = "out:" + s.getvalue()
except Exception as e:
	print "entered error"
	resp = traceback.format_exc()
	print >> temp
#print resp
print resp
print >> sys.stdout
print >> sys.stderr