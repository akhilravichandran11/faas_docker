import sys
import StringIO
import contextlib
import traceback

code = """
def madhat_func(data):
    i = [0,1]
    for j in i :
        data["val"] = data["val"]+ j
        print "Inside Madhat " + str(data["val"])
    d = i[2]
"""
main_code = """
madhat_func(data)
"""
data = {
    "val" : 2
}
resp = ""

@contextlib.contextmanager
def stdoutIO(flag,stdout = None):
     if flag:
         old = sys.stdout
     else:
             old=sys.stderr
     if stdout is None:
         stdout = StringIO.StringIO()
     if flag:
          sys.stdout = stdout
     else:
         sys.stderr=stdout
     try:
         yield stdout
     finally:
         if flag:
             sys.stdout = old
         else:
             sys.stderr=old


try:
    print ('Before Data ='  + str(data))
    with stdoutIO(flag=True) as s, stdoutIO(flag=False) as t:
        print ("Started Context Manager")
        exec(code+main_code,{"data":data})
        print ("Ended Context Manager")
    print ("After Data = " + str(data))
    print ("Start Output :\n") 
    print (s.getvalue())
    print (t.getvalue()) 
    print ("End Output \n")
except Exception as e:
    print ("Entered Exception :\n")
    print (traceback.format_exc())
    print ("Completed Exception \n")
#print resp
