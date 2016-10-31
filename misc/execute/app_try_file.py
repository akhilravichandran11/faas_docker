import sys
import os
import StringIO
import contextlib
import traceback

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


f = open("myfile.log", "w")
original_stderr = sys.stderr
sys.stderr = f

f_1 = open("myfile.out", "w")
original_stdout = sys.stdout
sys.stdout = f_1

print "Dude Start"
try:
	print "Before Data = " + str(data)
	exec(code+main_code_2,{"data":data})
	print "After Data = " + str(data)
except Exception as e:
	print "Entered Exception"
	print traceback.format_exc()
	print "Completed Exception"
print "Dude End"

sys.stderr = original_stderr
f.close()

sys.stout = original_stdout
f_1.close()

#sys.stdout.write("no error\n")
#sys.stderr.write("fatal error\n")
#print "sdtout = " + str(sys.stdout.flush())
#print "stderr = " + str(sys.stderr.flush())
