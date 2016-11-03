import sys
import StringIO
import contextlib
import traceback

code = """
import traceback
def madhat_func(data):
	i = [0,1]
	for j in i :
		data["val"] = data["val"]+ j
		print "Inside Madhat " + str(data["val"])
	d = 1/0
"""
main_code = """
try:
	madhat_func(data)
except Exception as e:
	data["execption"]=traceback.format_exc()
"""
data = {
	"val" : 2
}
resp = ""

@contextlib.contextmanager
def stdoutIO(stdout = None,stderr = None):
	old = sys.stdout
	olde = sys.stderr
	if stdout is None:
		stdout = StringIO.StringIO()
		stderr = StringIO.StringIO()
	sys.stdout = stdout
	sys.stderr = stderr
	try:
		yield [stdout,stderr]
	except Exception as e:
		sys.stdout = old
		sys.stderr = olde
	finally:
		sys.stdout = old
		sys.stderr = olde

s = ""
try:
	print "Before Data = " + str(data)
	with stdoutIO() as s:
		print "Started Context Manager"
		exec(code+main_code,{"data":data})
		print "Ended Context Manager"
	print "After Data = " + str(data)
	print "Start Output :\n" 
#	print s[0].getvalue()
#	print s[1].getvalue()
	print "End Output \n"
except Exception as e:
	print "Entered Exception :\n"
	print traceback.format_exc()
	print "Completed Exception \n"
finally:
	print "In Finally : "
	print s[0].getvalue()
#	print s[1].getvalue()
	print "dude "