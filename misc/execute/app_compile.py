#!/usr/bin/python
import sys
import StringIO
import contextlib
import traceback
code_test_1 = """
def fib_iterative(n):
	i = 0
	j = 1
	k = 0
	while(n>0):
		k = i + j
		i = j
		j = k
		n = n -1
	return k
global fib_iterative
def madhat_func(input_data,output_data):
	i = [0,1]
	val = input_data["val"]
	for j in i :
		val = val+ j
		print "Inside Madhat " + str(val)
	output_data["val"]=val
	output_data["val_fib_non_iter_1"]=fib_iterative(7)
"""
success = True
output_text = ""
try:
	compile(code_test_1,"code_test","exec")
except Exception as e:
	success = False
	output_text = traceback.format_exc()
finally:
	run_details = ( "Compiled Succesfully" if(success) else "Compilation Exceptions" )
	return_data = dict(
		requestStatus = run_details,
		result = output_text
	)

#print output_text
print " Dude"
	
