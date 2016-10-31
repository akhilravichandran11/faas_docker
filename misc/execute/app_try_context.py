import sys
import StringIO
import contextlib
import traceback

code = """
def madhat_func(data):
	i = [0,1]
	for j in i :
		d = 1/0
		data["val"] = data["val"]+ j
		print "Inside Madhat " + str(data["val"])
"""
main_code = """
madhat_func(data)
"""
data = {
	"val" : 2
}
resp = ""

@contextlib.contextmanager
def stdoutIO(stdout = None):
	old = sys.stdout
	if stdout is None:
		stdout = StringIO.StringIO()
	sys.stdout = stdout
	try:
		yield stdout
	finally:
		sys.stdout = old


try:
	print "Before Data = " + str(data)
	with stdoutIO() as s:
		print "Started Context Manager"
		exec(code+main_code,{"data":data})
		print "Ended Context Manager"
	print "After Data = " + str(data)
	print "Start Output :\n" 
	print s.getvalue()
	print "End Output \n"
except Exception as e:
	print "Entered Exception :\n"
	print traceback.format_exc()
	print "Completed Exception \n"
#print resp
