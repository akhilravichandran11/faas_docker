#!/usr/bin/python
import sys
import subprocess
global_vars = {
	"dude_1" : "dude whats happening 1"
}
local_vars = {
	"dude_2" : "dude whats happening 2"
}

with open("output.txt", "wb") as f:
	subprocess.check_call(["python", "madfile_2.py"],stdout=f )
with stdoutIO() as f:
	subprocess.check_call(["python", "madfile_2.py"],stdout=f )

	
#print resp
	
