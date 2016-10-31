import sys
import os
import StringIO
import contextlib
import traceback


class RedirectStdStreams2(object):
	def __init__(self, stdout=None, stderr=None):
		self._stdout = stdout or sys.stdout
		self._stderr = stderr or sys.stderr

	def __enter__(self):
		self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
		self.old_stdout.flush(); self.old_stderr.flush()
		sys.stdout, sys.stderr = self._stdout, self._stderr

	def __exit__(self, exc_type, exc_value, traceback):
		self._stdout.flush(); self._stderr.flush()
		sys.stdout = self.old_stdout
		sys.stderr = self.old_stderr

code = """
def madhat_func(data):
	i = [0,1]
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

class RedirectStdStreams(object):
	def __init__(self, stdout = StringIO.StringIO(), stderr = StringIO.StringIO()):
		self._stdout = stdout
		self._stderr = stderr

	def __enter__(self):
		self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
		self.old_stdout.flush(); self.old_stderr.flush()
		sys.stdout, sys.stderr = self._stdout, self._stderr

	def __exit__(self, exc_type, exc_value, traceback):
		sys.stdout = self.old_stdout
		sys.stderr = self.old_stderr
		return True
resp = ""
devnull = open(os.devnull, 'w')
print "Dude Start"
try:
	print "Before Data = " + str(data)
	with RedirectStdStreams():
		print "dude 3"
		exec(code+main_code_2,{"data":data})
	print "After Data = " + str(data)
except Exception as e:
	print "Entered Exception"
	print traceback.format_exc()
	print "Completed Exception"
print "Dude End"

#sys.stdout.write("no error\n")
#sys.stderr.write("fatal error\n")
#print "sdtout = " + str(sys.stdout.flush())
#print "stderr = " + str(sys.stderr.flush())
