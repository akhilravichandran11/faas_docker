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
def stdoutIO(stdout = None):
	old = sys.stdout
	if stdout is None:
		stdout = StringIO.StringIO()
	sys.stdout = stdout
	try:
		yield stdout
	finally:
		sys.stdout = old
output_text = ""
try:
	print "Before Data = " + str(data)
	with stdoutIO() as s:
		print "Started Context Manager"
		exec(code+main_code,{"data":data})
		print "Ended Context Manager"
	print "After Data = " + str(data)
	print "Start Output :\n" 
	output_text = s.getvalue()
	output_text = output_text +data["execption"]
	print "End Output \n"
except Exception as e:
	print "Entered Exception :\n"
	output_text = traceback.format_exc()
	print "Completed Exception \n"
finally:
	print "In Finally : "
	print output_text
	print "dude "